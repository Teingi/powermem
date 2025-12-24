"""
Agent service for PowerMem API
"""

import logging
from typing import Any, Dict, List, Optional
from powermem import auto_config
from powermem.agent import AgentMemory
from ..models.errors import ErrorCode, APIError

logger = logging.getLogger("server")


class AgentService:
    """Service for agent memory operations"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize agent service.
        
        Args:
            config: PowerMem configuration (uses auto_config if None)
        """
        if config is None:
            config = auto_config()
        
        self.agent_memory = AgentMemory(config=config)
        logger.info("AgentService initialized")
    
    def get_agent_memories(
        self,
        agent_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get all memories for an agent.
        
        Args:
            agent_id: Agent ID
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of memories
            
        Raises:
            APIError: If retrieval fails
        """
        try:
            if not agent_id:
                raise APIError(
                    code=ErrorCode.INVALID_REQUEST,
                    message="agent_id is required",
                    status_code=400,
                )
            
            # AgentMemory.get_all() doesn't support offset, so we need to handle it manually
            all_memories = self.agent_memory.get_all(
                agent_id=agent_id,
                limit=limit + offset,  # Get more results to account for offset
            )
            
            # Apply offset manually
            if offset > 0 and len(all_memories) > offset:
                memories = all_memories[offset:offset + limit]
            elif offset > 0:
                memories = []
            else:
                memories = all_memories[:limit]
            
            return memories
            
        except APIError:
            raise
        except Exception as e:
            logger.error(f"Failed to get agent memories {agent_id}: {e}", exc_info=True)
            raise APIError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Failed to get agent memories: {str(e)}",
                status_code=500,
            )
    
    def create_agent_memory(
        self,
        agent_id: str,
        content: str,
        user_id: Optional[str] = None,
        run_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        filters: Optional[Dict[str, Any]] = None,
        scope: Optional[str] = None,
        memory_type: Optional[str] = None,
        infer: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a memory for an agent.
        
        Uses AgentMemory system for intelligent memory management with
        multi-agent collaboration, permissions, and scope support.
        
        Args:
            agent_id: Agent ID
            content: Memory content
            user_id: User ID
            run_id: Run ID (stored in metadata)
            metadata: Metadata
            filters: Filters (stored in metadata)
            scope: Memory scope (e.g., 'AGENT', 'USER_GROUP', 'PUBLIC')
            memory_type: Memory type (stored in metadata)
            infer: Deprecated - AgentMemory handles intelligent processing internally
            
        Returns:
            Created memory data with memory_id field
            
        Raises:
            APIError: If creation fails
        """
        try:
            if not agent_id:
                raise APIError(
                    code=ErrorCode.INVALID_REQUEST,
                    message="agent_id is required",
                    status_code=400,
                )
            
            # Prepare metadata with run_id and other fields if provided
            enhanced_metadata = metadata or {}
            if run_id:
                enhanced_metadata["run_id"] = run_id
            if filters:
                enhanced_metadata["filters"] = filters
            if memory_type:
                enhanced_metadata["memory_type"] = memory_type
            
            # AgentMemory.add() returns a dict with memory information
            result = self.agent_memory.add(
                content=content,
                user_id=user_id,
                agent_id=agent_id,
                metadata=enhanced_metadata,
                scope=scope,
            )
            
            # Ensure memory_id field exists (use "id" from result)
            if isinstance(result, dict):
                if "id" in result and "memory_id" not in result:
                    result["memory_id"] = result["id"]
                logger.info(f"Agent memory created: {result.get('memory_id')} for agent {agent_id}")
                return result
            else:
                logger.error(f"Failed to create memory for agent {agent_id}: unexpected result type={type(result)}")
                raise APIError(
                    code=ErrorCode.MEMORY_CREATE_FAILED,
                    message="No memory was created. Unexpected result format.",
                    status_code=500,
                )
            
        except APIError:
            raise
        except Exception as e:
            logger.error(f"Failed to create agent memory: {e}", exc_info=True)
            raise APIError(
                code=ErrorCode.MEMORY_CREATE_FAILED,
                message=f"Failed to create agent memory: {str(e)}",
                status_code=500,
            )
    
    def share_memories(
        self,
        agent_id: str,
        target_agent_id: str,
        memory_ids: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Share memories between agents.
        
        Uses AgentMemory's share_memory method for proper memory sharing
        between agents with permission and collaboration support.
        
        Args:
            agent_id: Source agent ID
            target_agent_id: Target agent ID
            memory_ids: Specific memory IDs to share (None for all)
            
        Returns:
            Sharing result
            
        Raises:
            APIError: If sharing fails
        """
        try:
            if not agent_id or not target_agent_id:
                raise APIError(
                    code=ErrorCode.INVALID_REQUEST,
                    message="agent_id and target_agent_id are required",
                    status_code=400,
                )
            
            # Get memories to share
            if memory_ids:
                # Get specific memories by ID
                memories = []
                all_memories = self.agent_memory.get_all(agent_id=agent_id)
                memory_id_set = set(memory_ids)
                for memory in all_memories:
                    mem_id = memory.get("id") or memory.get("memory_id")
                    if mem_id in memory_id_set:
                        memories.append(memory)
            else:
                memories = self.agent_memory.get_all(agent_id=agent_id)
            
            # Use AgentMemory's share_memory method for proper sharing
            shared_count = 0
            for memory in memories:
                try:
                    mem_id = memory.get("id") or memory.get("memory_id")
                    if not mem_id:
                        continue
                    
                    # Use the share_memory method if available
                    if hasattr(self.agent_memory, 'share_memory'):
                        share_result = self.agent_memory.share_memory(
                            memory_id=str(mem_id),
                            from_agent=agent_id,
                            to_agents=[target_agent_id],
                        )
                        if share_result.get("success", False):
                            shared_count += 1
                    else:
                        # Fallback: copy memory to target agent
                        self.agent_memory.add(
                            content=memory.get("content") or memory.get("memory", ""),
                            user_id=memory.get("user_id"),
                            agent_id=target_agent_id,
                            metadata=memory.get("metadata", {}),
                            scope=memory.get("scope"),
                        )
                        shared_count += 1
                except Exception as e:
                    logger.warning(f"Failed to share memory {memory.get('memory_id')}: {e}")
            
            logger.info(f"Shared {shared_count} memories from {agent_id} to {target_agent_id}")
            
            return {
                "shared_count": shared_count,
                "source_agent_id": agent_id,
                "target_agent_id": target_agent_id,
            }
            
        except APIError:
            raise
        except Exception as e:
            logger.error(f"Failed to share memories: {e}", exc_info=True)
            raise APIError(
                code=ErrorCode.AGENT_MEMORY_SHARE_FAILED,
                message=f"Failed to share memories: {str(e)}",
                status_code=500,
            )
    
    def get_shared_memories(
        self,
        agent_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get shared memories for an agent.
        
        Note: This is a simplified implementation. Full implementation would
        track sharing relationships.
        
        Args:
            agent_id: Agent ID
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of shared memories
        """
        # For now, return all memories for the agent
        # In a full implementation, this would filter for shared memories only
        return self.get_agent_memories(agent_id, limit, offset)
