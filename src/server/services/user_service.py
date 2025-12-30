"""
User service for PowerMem API
"""

import logging
from typing import Any, Dict, List, Optional
from powermem import UserMemory, auto_config
from ..models.errors import ErrorCode, APIError

logger = logging.getLogger("server")


class UserService:
    """Service for user profile operations"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize user service.
        
        Args:
            config: PowerMem configuration (uses auto_config if None)
        """
        if config is None:
            config = auto_config()
        
        self.user_memory = UserMemory(config=config)
        logger.info("UserService initialized")
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get user profile.
        
        Args:
            user_id: User ID
            
        Returns:
            User profile data
            
        Raises:
            APIError: If profile not found or retrieval fails
        """
        try:
            if not user_id:
                raise APIError(
                    code=ErrorCode.INVALID_REQUEST,
                    message="user_id is required",
                    status_code=400,
                )
            
            profile = self.user_memory.profile_store.get_profile_by_user_id(user_id)
            
            if not profile:
                raise APIError(
                    code=ErrorCode.USER_NOT_FOUND,
                    message=f"User profile for {user_id} not found",
                    status_code=404,
                )
            
            return profile
            
        except APIError:
            raise
        except Exception as e:
            logger.error(f"Failed to get user profile {user_id}: {e}", exc_info=True)
            raise APIError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Failed to get user profile: {str(e)}",
                status_code=500,
            )
    
    def update_user_profile(
        self,
        user_id: str,
        profile_content: Optional[str] = None,
        topics: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update user profile.
        
        Args:
            user_id: User ID
            profile_content: Profile content text
            topics: Structured topics dictionary
            
        Returns:
            Updated profile data
            
        Raises:
            APIError: If update fails
        """
        try:
            if not user_id:
                raise APIError(
                    code=ErrorCode.INVALID_REQUEST,
                    message="user_id is required",
                    status_code=400,
                )
            
            # Save profile
            profile_id = self.user_memory.profile_store.save_profile(
                user_id=user_id,
                profile_content=profile_content,
                topics=topics,
            )
            
            # Get updated profile
            profile = self.user_memory.profile_store.get_profile_by_user_id(user_id)
            
            logger.info(f"User profile updated: {user_id}")
            return profile
            
        except APIError:
            raise
        except Exception as e:
            logger.error(f"Failed to update user profile {user_id}: {e}", exc_info=True)
            raise APIError(
                code=ErrorCode.PROFILE_UPDATE_FAILED,
                message=f"Failed to update user profile: {str(e)}",
                status_code=500,
            )
    
    def get_user_memories(
        self,
        user_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get all memories for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of memories
        """
        try:
            if not user_id:
                raise APIError(
                    code=ErrorCode.INVALID_REQUEST,
                    message="user_id is required",
                    status_code=400,
                )
            
            result = self.user_memory.memory.get_all(
                user_id=user_id,
                limit=limit,
                offset=offset,
            )
            
            # get_all returns a dict with "results" key, extract the list
            if isinstance(result, dict):
                memories = result.get("results", [])
            elif isinstance(result, list):
                memories = result
            else:
                memories = []
            
            return memories
            
        except APIError:
            raise
        except Exception as e:
            logger.error(f"Failed to get user memories {user_id}: {e}", exc_info=True)
            raise APIError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Failed to get user memories: {str(e)}",
                status_code=500,
            )
    
    def delete_user_memories(self, user_id: str) -> Dict[str, Any]:
        """
        Delete all memories for a user (user profile deletion).
        
        Args:
            user_id: User ID
            
        Returns:
            Deletion result
            
        Raises:
            APIError: If deletion fails
        """
        try:
            if not user_id:
                raise APIError(
                    code=ErrorCode.INVALID_REQUEST,
                    message="user_id is required",
                    status_code=400,
                )
            
            # Get all memories for the user
            result = self.user_memory.memory.get_all(user_id=user_id)
            
            # get_all returns a dict with "results" key, extract the list
            if isinstance(result, dict):
                memories = result.get("results", [])
            elif isinstance(result, list):
                memories = result
            else:
                memories = []
            
            deleted_count = 0
            failed_count = 0
            
            for memory in memories:
                try:
                    # Ensure memory is a dict before accessing
                    if not isinstance(memory, dict):
                        logger.warning(f"Skipping invalid memory format: {type(memory)}")
                        failed_count += 1
                        continue
                    
                    memory_id = memory.get("id") or memory.get("memory_id")
                    if memory_id:
                        success = self.user_memory.memory.delete(
                            memory_id=memory_id,
                            user_id=user_id,
                        )
                        if success:
                            deleted_count += 1
                        else:
                            failed_count += 1
                    else:
                        logger.warning(f"Memory missing ID: {memory}")
                        failed_count += 1
                except Exception as e:
                    memory_id_str = str(memory.get('id', 'unknown')) if isinstance(memory, dict) else 'unknown'
                    logger.warning(f"Failed to delete memory {memory_id_str}: {e}")
                    failed_count += 1
            
            logger.info(f"Deleted {deleted_count} memories for user {user_id}")
            
            return {
                "user_id": user_id,
                "deleted_count": deleted_count,
                "failed_count": failed_count,
                "total": len(memories),
            }
            
        except APIError:
            raise
        except Exception as e:
            logger.error(f"Failed to delete user memories {user_id}: {e}", exc_info=True)
            raise APIError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Failed to delete user memories: {str(e)}",
                status_code=500,
            )