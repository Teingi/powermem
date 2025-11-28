# Ebbinghaus Forgetting Curve - Automatic Usage Explained

## Overview

This document clarifies how the Ebbinghaus forgetting curve is automatically applied in PowerMem's intelligent memory system, addressing common confusion about whether manual calculation is required.

## Key Answer: It's Automatic!

**The Ebbinghaus forgetting curve is automatically applied to search results when intelligent memory is enabled.** You do NOT need to manually calculate decay or sort results yourself.

## How It Works Automatically

### 1. Configuration Setup

When you configure your `.env` file with:

```env
MEMORY_DECAY_ENABLED=true
MEMORY_DECAY_ALGORITHM=ebbinghaus
MEMORY_DECAY_BASE_RETENTION=1.0
MEMORY_DECAY_FORGETTING_RATE=0.1
MEMORY_DECAY_REINFORCEMENT_FACTOR=0.3
```

**Note:** These `MEMORY_DECAY_*` variables are legacy names. The current implementation uses `INTELLIGENT_MEMORY_*` variables. However, both work if properly mapped in your configuration.

The recommended `.env` configuration is:

```env
INTELLIGENT_MEMORY_ENABLED=true
INTELLIGENT_MEMORY_DECAY_RATE=0.1
INTELLIGENT_MEMORY_INITIAL_RETENTION=1.0
INTELLIGENT_MEMORY_REINFORCEMENT_FACTOR=0.3
```

### 2. Automatic Application Flow

When you call `memory.search()`, the following happens automatically:

```
1. User calls: memory.search(query="...")
   ↓
2. Memory.search() performs vector similarity search
   ↓
3. If intelligent_memory.enabled == True:
   ↓
4. IntelligenceManager.process_search_results() is called
   ↓
5. IntelligentMemoryManager.process_search_results() applies:
   - Calculates relevance_score for each result
   - Calculates decay_factor using Ebbinghaus formula
   - Computes final_score = relevance_score × decay_factor
   - Re-sorts results by final_score (descending)
   ↓
6. Returns automatically sorted results
```

### 3. Code Implementation

The automatic decay is implemented in `IntelligentMemoryManager.process_search_results()`:

```python
def process_search_results(self, results: List[Dict[str, Any]], query: str):
    processed_results = []
    for result in results:
        # Calculate relevance score
        relevance_score = self.ebbinghaus_algorithm.calculate_relevance(result, query)
        
        # Apply decay based on age (AUTOMATIC)
        decay_factor = self.ebbinghaus_algorithm.calculate_decay(
            result.get("created_at", datetime.utcnow())
        )
        
        # Combine scores
        processed_result = result.copy()
        processed_result["relevance_score"] = relevance_score
        processed_result["decay_factor"] = decay_factor
        processed_result["final_score"] = relevance_score * decay_factor
        
        processed_results.append(processed_result)
    
    # AUTOMATICALLY sort by final_score
    processed_results.sort(key=lambda x: x["final_score"], reverse=True)
    
    return processed_results
```

This is called automatically in `Memory.search()`:

```python
def search(self, query: str, ...):
    # ... perform vector search ...
    
    # AUTOMATIC processing if intelligent memory enabled
    if self.intelligence.enabled:
        processed_results = self.intelligence.process_search_results(results, query)
    else:
        processed_results = results
    
    return {"results": processed_results}
```

## What You DON'T Need to Do

❌ **You do NOT need to:**
- Manually calculate decay factors after search
- Manually sort results by retention scores
- Implement your own forgetting curve logic
- Call decay calculation functions yourself

✅ **You just need to:**
- Enable intelligent memory in config
- Call `memory.search()` normally
- Results are automatically ranked by combined score (similarity × retention)

## When Manual Calculation is Shown in Documentation

The documentation examples showing manual calculation (like in `scenario_8_ebbinghaus_forgetting_curve.md`) are for:

1. **Educational purposes**: Understanding how the curve works
2. **Custom use cases**: When you want to build your own ranking logic
3. **Analysis**: When you want to analyze retention scores separately
4. **Visualization**: Creating charts of the forgetting curve

These are **optional** and **not required** for normal usage.

## Verification: Is It Working?

To verify that automatic decay is working:

### Method 1: Check Configuration

```python
from powermem import Memory, auto_config

config = auto_config()
memory = Memory(config=config)

# Check if intelligent memory is enabled
print(f"Intelligent memory enabled: {memory.intelligence.enabled}")
print(f"Intelligent memory manager: {memory.intelligence.intelligent_memory_manager is not None}")
```

### Method 2: Inspect Search Results

```python
results = memory.search(query="your query", user_id="user1")

# Check if results have decay_factor and final_score
for result in results.get("results", [])[:3]:
    print(f"Score: {result.get('score')}")
    print(f"Decay factor: {result.get('decay_factor', 'N/A')}")
    print(f"Final score: {result.get('final_score', 'N/A')}")
    print("---")
```

If you see `decay_factor` and `final_score` in results, automatic decay is working!

### Method 3: Compare Old vs New Memories

```python
# Add an old memory (simulated)
old_memory = memory.add(
    messages="This is an old memory",
    user_id="user1",
    metadata={"created_at": (datetime.now() - timedelta(days=30)).isoformat()}
)

# Add a new memory
new_memory = memory.add(
    messages="This is a new memory",
    user_id="user1"
)

# Search - new memory should rank higher even with same similarity
results = memory.search(query="memory", user_id="user1")
# New memory should appear first due to higher retention
```

## Configuration Mapping

### Legacy Variables (MEMORY_DECAY_*)

If you're using `MEMORY_DECAY_*` variables, they need to be mapped to `intelligent_memory` config:

```python
# Manual mapping if needed
config = {
    "intelligent_memory": {
        "enabled": os.getenv("MEMORY_DECAY_ENABLED", "true").lower() == "true",
        "decay_rate": float(os.getenv("MEMORY_DECAY_FORGETTING_RATE", "0.1")),
        "initial_retention": float(os.getenv("MEMORY_DECAY_BASE_RETENTION", "1.0")),
        "reinforcement_factor": float(os.getenv("MEMORY_DECAY_REINFORCEMENT_FACTOR", "0.3")),
    }
}
```

### Recommended Variables (INTELLIGENT_MEMORY_*)

Use these in your `.env` file:

```env
INTELLIGENT_MEMORY_ENABLED=true
INTELLIGENT_MEMORY_DECAY_RATE=0.1
INTELLIGENT_MEMORY_INITIAL_RETENTION=1.0
INTELLIGENT_MEMORY_REINFORCEMENT_FACTOR=0.3
INTELLIGENT_MEMORY_WORKING_THRESHOLD=0.3
INTELLIGENT_MEMORY_SHORT_TERM_THRESHOLD=0.6
INTELLIGENT_MEMORY_LONG_TERM_THRESHOLD=0.8
```

## Summary

1. **Automatic**: Ebbinghaus decay is automatically applied to search results
2. **No manual work**: You don't need to calculate or sort manually
3. **Configuration**: Just enable `INTELLIGENT_MEMORY_ENABLED=true`
4. **Transparent**: Results are automatically re-ranked by `final_score = similarity × retention`
5. **Documentation examples**: Manual calculation examples are for learning, not required usage

The forgetting curve logic is **already included by default** when intelligent memory is enabled!

