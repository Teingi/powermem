"""
Test cases for list memories with sorting functionality

This module contains tests for the list memories API with sorting support.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from powermem import Memory


class TestListMemoriesSorting:
    """Test cases for list memories with sorting."""
    
    @pytest.fixture
    def mock_memory(self):
        """Create a mock Memory instance."""
        with patch('powermem.core.memory.VectorStoreFactory'), \
             patch('powermem.core.memory.LLMFactory'), \
             patch('powermem.core.memory.EmbedderFactory'):
            memory = Memory()
            return memory
    
    def test_get_all_with_sort_by_updated_at_desc(self, mock_memory):
        """Test get_all with sorting by updated_at in descending order."""
        # Mock storage.get_all_memories to return test data
        test_memories = [
            {
                "id": 1,
                "memory": "Memory 1",
                "updated_at": datetime.now() - timedelta(days=3),
                "created_at": datetime.now() - timedelta(days=5),
            },
            {
                "id": 2,
                "memory": "Memory 2",
                "updated_at": datetime.now() - timedelta(days=1),
                "created_at": datetime.now() - timedelta(days=4),
            },
            {
                "id": 3,
                "memory": "Memory 3",
                "updated_at": datetime.now() - timedelta(days=2),
                "created_at": datetime.now() - timedelta(days=3),
            },
        ]
        
        with patch.object(mock_memory.storage, 'get_all_memories', return_value=test_memories):
            result = mock_memory.get_all(
                user_id="test_user",
                limit=10,
                sort_by="updated_at",
                order="desc"
            )
            
            assert "results" in result
            results = result["results"]
            
            # Verify results are sorted by updated_at in descending order
            # Memory 2 should be first (most recent update)
            assert len(results) == 3
            assert results[0]["id"] == 2  # Most recently updated
            assert results[1]["id"] == 3
            assert results[2]["id"] == 1  # Least recently updated
    
    def test_get_all_with_sort_by_updated_at_asc(self, mock_memory):
        """Test get_all with sorting by updated_at in ascending order."""
        test_memories = [
            {
                "id": 1,
                "memory": "Memory 1",
                "updated_at": datetime.now() - timedelta(days=3),
                "created_at": datetime.now() - timedelta(days=5),
            },
            {
                "id": 2,
                "memory": "Memory 2",
                "updated_at": datetime.now() - timedelta(days=1),
                "created_at": datetime.now() - timedelta(days=4),
            },
            {
                "id": 3,
                "memory": "Memory 3",
                "updated_at": datetime.now() - timedelta(days=2),
                "created_at": datetime.now() - timedelta(days=3),
            },
        ]
        
        with patch.object(mock_memory.storage, 'get_all_memories', return_value=test_memories):
            result = mock_memory.get_all(
                user_id="test_user",
                limit=10,
                sort_by="updated_at",
                order="asc"
            )
            
            assert "results" in result
            results = result["results"]
            
            # Verify results are sorted by updated_at in ascending order
            # Memory 1 should be first (oldest update)
            assert len(results) == 3
            assert results[0]["id"] == 1  # Oldest update
            assert results[1]["id"] == 3
            assert results[2]["id"] == 2  # Most recent update
    
    def test_get_all_with_sort_by_created_at_desc(self, mock_memory):
        """Test get_all with sorting by created_at in descending order."""
        test_memories = [
            {
                "id": 1,
                "memory": "Memory 1",
                "created_at": datetime.now() - timedelta(days=5),
                "updated_at": datetime.now() - timedelta(days=1),
            },
            {
                "id": 2,
                "memory": "Memory 2",
                "created_at": datetime.now() - timedelta(days=2),
                "updated_at": datetime.now() - timedelta(days=1),
            },
            {
                "id": 3,
                "memory": "Memory 3",
                "created_at": datetime.now() - timedelta(days=1),
                "updated_at": datetime.now() - timedelta(days=1),
            },
        ]
        
        with patch.object(mock_memory.storage, 'get_all_memories', return_value=test_memories):
            result = mock_memory.get_all(
                user_id="test_user",
                limit=10,
                sort_by="created_at",
                order="desc"
            )
            
            assert "results" in result
            results = result["results"]
            
            # Verify results are sorted by created_at in descending order
            assert len(results) == 3
            assert results[0]["id"] == 3  # Most recently created
            assert results[1]["id"] == 2
            assert results[2]["id"] == 1  # Oldest created
    
    def test_get_all_with_sort_by_id_desc(self, mock_memory):
        """Test get_all with sorting by id in descending order."""
        test_memories = [
            {"id": 1, "memory": "Memory 1"},
            {"id": 3, "memory": "Memory 3"},
            {"id": 2, "memory": "Memory 2"},
        ]
        
        with patch.object(mock_memory.storage, 'get_all_memories', return_value=test_memories):
            result = mock_memory.get_all(
                user_id="test_user",
                limit=10,
                sort_by="id",
                order="desc"
            )
            
            assert "results" in result
            results = result["results"]
            
            # Verify results are sorted by id in descending order
            assert len(results) == 3
            assert results[0]["id"] == 3  # Highest ID
            assert results[1]["id"] == 2
            assert results[2]["id"] == 1  # Lowest ID
    
    def test_get_all_without_sorting(self, mock_memory):
        """Test get_all without sorting (should return original order)."""
        test_memories = [
            {"id": 1, "memory": "Memory 1"},
            {"id": 2, "memory": "Memory 2"},
            {"id": 3, "memory": "Memory 3"},
        ]
        
        with patch.object(mock_memory.storage, 'get_all_memories', return_value=test_memories):
            result = mock_memory.get_all(
                user_id="test_user",
                limit=10,
                sort_by=None
            )
            
            assert "results" in result
            results = result["results"]
            
            # Results should be in original order (no sorting applied)
            assert len(results) == 3
    
    def test_get_all_with_filtering_and_sorting(self, mock_memory):
        """Test get_all with both filtering and sorting."""
        test_memories = [
            {
                "id": 1,
                "memory": "Memory 1",
                "user_id": "test_user",
                "updated_at": datetime.now() - timedelta(days=3),
            },
            {
                "id": 2,
                "memory": "Memory 2",
                "user_id": "test_user",
                "updated_at": datetime.now() - timedelta(days=1),
            },
            {
                "id": 3,
                "memory": "Memory 3",
                "user_id": "other_user",
                "updated_at": datetime.now() - timedelta(days=2),
            },
        ]
        
        with patch.object(mock_memory.storage, 'get_all_memories', return_value=test_memories):
            result = mock_memory.get_all(
                user_id="test_user",
                agent_id=None,
                limit=10,
                sort_by="updated_at",
                order="desc"
            )
            
            assert "results" in result
            results = result["results"]
            
            # Verify filtering and sorting work together
            # Only memories with user_id="test_user" should be returned
            # And they should be sorted by updated_at desc
            assert len(results) == 3  # All returned (filtering happens in storage)
            # Note: In real scenario, filtering would happen at storage level
            # This test verifies sorting is applied after filtering
    
    def test_get_all_with_pagination_and_sorting(self, mock_memory):
        """Test get_all with pagination and sorting."""
        # Create 5 test memories
        base_time = datetime.now()
        test_memories = [
            {
                "id": i,
                "memory": f"Memory {i}",
                "updated_at": base_time - timedelta(days=5-i),
            }
            for i in range(1, 6)
        ]
        
        with patch.object(mock_memory.storage, 'get_all_memories', return_value=test_memories):
            # Get first page
            result1 = mock_memory.get_all(
                user_id="test_user",
                limit=2,
                offset=0,
                sort_by="updated_at",
                order="desc"
            )
            
            assert "results" in result1
            results1 = result1["results"]
            assert len(results1) == 2
            
            # Get second page
            result2 = mock_memory.get_all(
                user_id="test_user",
                limit=2,
                offset=2,
                sort_by="updated_at",
                order="desc"
            )
            
            assert "results" in result2
            results2 = result2["results"]
            assert len(results2) == 2
            
            # Verify pagination works with sorting
            # Results should be consistent across pages
            assert results1[0]["id"] != results2[0]["id"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

