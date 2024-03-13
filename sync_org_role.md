
# Sync org roles

  ```mermaid
  sequenceDiagram

      participant A as client
      participant B as BackendAPI
      participant V as VSAPI


      A->>B: request
      B->>B: leave_room(sid,lesson_id)
      B->>R: update "alive:org_{org_id}_user_{user_id}" key {state:disconnect}
      B->>B:call mixpanel disconnect
      B->>M: emit "teacher_disconnect"  {"user_id": client_id}

  ```