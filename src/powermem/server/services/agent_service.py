"""
Agent service for PowerMem API
"""

import logging
from typing import Any, Dict, List, Optional
from powermem import Memory, auto_config
from ..models.errors import ErrorCode, APIError

logger = logging.getLogger("powermem.server")


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
        
        self.memory = Memory(config=config)
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
            
            memories = self.memory.get_all(
                agent_id=agent_id,
                limit=limit,
                offset=offset,
            )
            
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
        
        Args:
            agent_id: Agent ID
            content: Memory content
            user_id: User ID
            run_id: Run ID
            metadata: Metadata
            filters: Filters
            scope: Scope
            memory_type: Memory type
            infer: Enable intelligent processing
            
        Returns:
            Created memory data
            
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
            
            result = self.memory.add(
                messages=content,
                user_id=user_id,
                agent_id=agent_id,
                run_id=run_id,
                metadata=metadata,
                filters=filters,
                scope=scope,
                memory_type=memory_type,
                infer=infer,
            )
            
            logger.info(f"Agent memory created: {result.get('memory_id')} for agent {agent_id}")
            return result
            
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
        
        Note: This is a placeholder implementation. Full agent memory sharing
        would require the AgentMemory system which is more complex.
        
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
                memories = []
                for memory_id in memory_ids:
                    try:
                        memory = self.memory.get(memory_id=memory_id, agent_id=agent_id)
                        if memory:
                            memories.append(memory)
                    except Exception:
                        pass
            else:
                memories = self.memory.get_all(agent_id=agent_id)
            
            # For now, we'll just copy the memories to the target agent
            # In a full implementation, this would use the AgentMemory sharing system
            shared_count = 0
            for memory in memories:
                try:
                    self.memory.add(
                        messages=memory.get("content", ""),
                        user_id=memory.get("user_id"),
                        agent_id=target_agent_id,
                        run_id=memory.get("run_id"),
                        metadata=memory.get("metadata", {}),
                        filters=memory.get("filters"),
                        scope=memory.get("scope"),
                        memory_type=memory.get("memory_type"),
                        infer=False,  # Don't re-process shared memories
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
