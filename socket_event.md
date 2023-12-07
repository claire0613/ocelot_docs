- # connect Event

  - ### queryString:

        role=teacher/student
        org_id={org_id}
        product_type= manager (optional)(manager_web need)
        auth=access_token

  - ## TeacherAPP

```mermaid
sequenceDiagram

        participant A as client
        participant B as BackendSocket
        participant R as Redis

        A->>B: connected
        B->>R:add "alive:org_{org_id}_user_{user_id}" key {login_time:int,state:connect}
        B->>R: set "user_id" key {"sid":sid,client_id": user_id,"role": role,"org_id": org_id}
        alt reconnected for mixpanel
            alt get_lesson_id
                B->>B:call mixpanel reconnect
                %% B->>R:check "lesson_room_{lesson_id}" key exists
                %%alt if not "lesson_room_{lesson_id}" key exists
                    %%B->>DB: query DB
                    %%DB->>B: room_id
                    %%B->>R: set lesson_room_{lesson_id}" key
                %%end

                %%B->>B:call mixpanel reconnect
            end

        end

```

- ## StudentWeb

```mermaid
sequenceDiagram

    participant A as client
    participant B as BackendSocket
    participant R as Redis
    A->>B: connected
    B->>R: set "user_id" key {"sid":sid,"client_id": user_id,"role": role,"org_id": org_id}
    alt reconnected

        alt get_lesson_id
            B->>B:call mixpanel reconnect
        end

    end

```

- ## ManagerWeb

```mermaid
sequenceDiagram

    participant A as client
    participant B as BackendSocket
    participant R as Redis
    A->>B: connected
    B->>R: set "manager:org_{org_id}_user_{user_id}" key {"sid":sid,client_id": user_id,"role": role,"org_id": org_id}
    alt reconnected
        alt get_lesson_id
            B->>B:call mixpanel reconnect
        end

    end

```

---

- # disconnect Event

  - ### queryString:
        role=teacher/student
        org_id={org_id}
        product_type= manager (optional)(manager_web need)
        auth=access_token

- ## TeacherAPP

```mermaid
sequenceDiagram

    participant A as client
    participant B as BackendSocket
    participant R as Redis
    A->>B: disconnected
    B->>B: leave_room(sid,lesson_id)
    B->>R: update "alive:org_{org_id}_user_{user_id}" key {state:disconnect}
    B->>B:call mixpanel disconnect

```

- ## StudentWeb/ ManagerWeb

```mermaid
sequenceDiagram

    participant A as client
    participant B as BackendSocket
    participant R as Redis
    A->>B: disconnected
    B->>B: leave_room(sid,lesson_id)
    B->>B:call mixpanel disconnect

```

- # join_lesson Event

  - ### data:

         {
            user_id:"",
            lesson_id:"",
            role:teacher/student
         }

- ## TeacherAPP

```mermaid
sequenceDiagram

    participant A as client
    participant B as BackendSocket
    participant R as Redis
    participant D as DB

    A->>B: join_lesson
    B->>D: check_lesson_exists
    alt if not lesson exists
        B->>A: failed
    end

    B->>R: check "lesson_seat_{lesson_id}"key
    alt if not lesson_seat_* exists
        B->>R: add "lesson_seat_*" key  {1:"",2:""....}
    end
    B->>R: add lesson_teacher_{lesson_id}"key {{user_id}:sid} & TTL 24hrs

```

- ## StudentWeb

```mermaid
sequenceDiagram

    participant A as client
    participant B as BackendSocket
    participant R as Redis
    participant D as DB

    A->>B: join_lesson
    B->>D: check_lesson_exists
    alt if not lesson exists
        B->>A: failed
    end

    B->>R: check "lesson_seat_{lesson_id}"key
    alt if not lesson_seat_* exists
        B->>R: add "lesson_seat_*" key  {1:"",2:""....}
    end
    B->>R: add lesson_student_{lesson_id}"key {{user_id}:sid}& TTL 24hrs

```

- # log_out Event

  - ### data:

         {
            user_id:"",
            org_id:"",
         }

- ## TeacherAPP

```mermaid
sequenceDiagram

    participant A as client
    participant B as BackendSocket
    participant R as Redis

    A->>B: log_out
    B->>R:remove "alive:org_{org_id}_user_{user_id}" key
    B->>A: emit all manager web in same org

```
