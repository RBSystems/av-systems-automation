Reindexing alone is pretty straight-forward
1. Create new index & mapping
2. Run reindex.py, modifying the to/from index names (line 14)

Recreating and massaging the index as a secondary index is another thing.
1. Create new index & mapping
2. Run rebuildWithNew.py to get all events from one index to another, re-mapping things via the doc element.
3. If needed:
    * Run deleteEvents.py with the correct index selected to remove erroneously-created events
    * Delete Index
    * Recreate Index