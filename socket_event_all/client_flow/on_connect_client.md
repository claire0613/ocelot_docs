
- Teacher APP
```mermaid
flowchart TD
    A[emit connect] --> B{Is it?}
    B -- Yes --> C[OK]
    C --> D[Rethink]
    D --> B
    B -- No ----> E[End]
```