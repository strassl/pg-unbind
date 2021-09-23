# pg-unbind

Hacky script to to create a query with inlined parameters from a query logged by postgres with bind parameters.
For debugging purposes only (useful if you want to EXPLAIN ANALYSE a slow query) -- under no circumstances should this be used for production purposes.
