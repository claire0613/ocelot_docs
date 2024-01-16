- # FLOW

  ### 老師上線登入

  ```mermaid
            sequenceDiagram

              participant A as client
              participant B as BackendSocket
              participant R as Redis
              participant M as ManagerWeb



              A->>B: 1. connected
              B->>R:2. add "alive:org_{org_id}_user_{user_id}" key {login_time:int,state:connect}
              B->>R:3.  set "user_id" key {"sid":sid,client_id": user_id,"role": role,"org_id": org_id}
              B->>M:4. emit "teacher_connect"  {"user_id": client_id}
  ```

  ### 老師登出

  ```mermaid
  sequenceDiagram

      participant A as TeacherAPP
      participant B as BackendSocket
      participant R as Redis
      participant M as ManagerWeb

      A->>B: 1. log_out
      B->>R: 2. remove "alive:org_{org_id}_user_{user_id}" key
      B->>M: 3. emit all manager web in same org  {"user_id":{user_id}}

  ```

  ### 老師斷線

  ```mermaid
  sequenceDiagram

      participant A as client
      participant B as BackendSocket
      participant R as Redis
      participant M as ManagerWeb


      A->>B: 1. disconnected
      B->>B: 2. leave_room(sid,lesson_id)
      B->>R: 3. update "alive:org_{org_id}_user_{user_id}" key {state:disconnect}
      B->>M: 4. emit "teacher_disconnect"  {"user_id": client_id}

  ```

  ### 老師加入 lesson

  ```mermaid
  sequenceDiagram

      participant A as client
      participant B as BackendSocket
      participant R as Redis
      A->>B: 1. join_lesson
      B->>B: 2. enter_room(sid,lesson_id)
      B->>R: 3. add lesson_teacher_{lesson_id}"key {{user_id}:sid} & TTL 24hrs

  ```

  ### Manager force logout 老師

  ```mermaid
  sequenceDiagram
      participant M as ManagerWeb
      participant B as BackendSocket
      participant R as Redis
      participant A as TeacherAPP

      M->>B: 1. force_logout
      B->>R: 2. set "cooldown:org_{org_id}_user_{user_id}" key & 5 mins TTL
      B->>R: 3. get "{user_id}" key to find TeacherAPP sid
      B->>A: 4. emit force_logout

  ```

  ### Redis pubsub

  ```mermaid
  sequenceDiagram
      participant B as BackendSocket
      participant R as Redis
      participant D as DB
      participant M as Manager


      R->>B: 1. listen "alive:org_{org_id}_user_{user_id}" key
      B->>D:2. do end lesson update lesson/quiz/task
      B->>M: 3. emit logout event

  ```

---

      socket connect ->“登入”
      socket disconnect ->“斷線”
      socket logout -> "登出”
      socket join_lesson -> “進入 lesson”
      socket set_student_name -> “學生選完座位後修改名字”

---

- # connect event

  **url: [backedn_domian]/classroom
  path: /sockets**

  - ### queryString:

        role=teacher/student
        org_id={org_id}
        product_type= manager (optional)(ManagerWeb need)
        auth=access_token

    - ex:
      - TeacherApp:
        ```
        role=teacher
        org_id={org_id}
        auth=access_token
        ```
      - StudentWeb:
        ```
        role=student
        auth=access_token
        ```
      - ManagerWeb:
        ```
        role=teacher/admin
        org_id={org_id}
        product_type= manager
        auth=access_token
        ```

  - ## TeacherAPP

    ```mermaid
    sequenceDiagram

            participant A as client
            participant B as BackendSocket
            participant R as Redis
            participant M as ManagerWeb



            A->>B: connected
            B->>R:add "alive:org_{org_id}_user_{user_id}" key {login_time:int,state:connect}
            B->>R: set "user_id" key {"sid":sid,client_id": user_id,"role": role,"org_id": org_id}
            B->>M: emit "teacher_connect"  {"user_id": client_id}
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
      B->>R: enter_room(room_id=org_id)
      alt reconnected
          alt get_lesson_id
              B->>B:call mixpanel reconnect
          end

      end

  ```

---

- # disconnect event
- ## TeacherAPP

  ```mermaid
  sequenceDiagram

      participant A as client
      participant B as BackendSocket
      participant R as Redis
      participant M as ManagerWeb


      A->>B: disconnected
      B->>B: leave_room(sid,lesson_id)
      B->>R: update "alive:org_{org_id}_user_{user_id}" key {state:disconnect}
      B->>B:call mixpanel disconnect
      B->>M: emit "teacher_disconnect"  {"user_id": client_id}

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

- # join_lesson event

  - ### client emit data:

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

- # logout event

  - ### client emit data:

         {
            user_id:"",
            org_id:"",
         }

  - ### listeners (client):

        - ManagerWeb
        listen event = "logout"

         {
            user_id:""
         }

- ## TeacherAPP

  ```mermaid
  sequenceDiagram

      participant A as TeacherAPP
      participant B as BackendSocket
      participant R as Redis
      participant M as ManagerWeb


      A->>B: 1. log_out
      B->>R: 2. remove "alive:org_{org_id}_user_{user_id}" key
      B->>M: 3. emit all manager web in same org  {"user_id":{user_id}}

  ```

- # force_logout event

  - ### client emit data:

         {
            user_id:"",
            org_id:"",
         }

  - ### listeners (client):

        - TeacherApp
        listen event = "force_logout"

         {
            user_id:""
         }

- ## ManagerWeb

  ```mermaid
  sequenceDiagram
      participant M as ManagerWeb
      participant B as BackendSocket
      participant R as Redis
      participant A as TeacherAPP

      M->>B: 1. force_logout
      B->>R: 2. set "cooldown:org_{org_id}_user_{user_id}" key & 5 mins TTL
      B->>R: 3. get "{user_id}" key to find TeacherAPP sid
      B->>A: 4. emit TeacherAPP


  ```

- # set_student_name event

  - ### client emit data:

         {
            lesson_id:"",
            display_name:"",
            seat_id:"",
            student_id:"",
         }

  - ### listeners (client):

        - TeacherApp
        listen event = "set_student_name"
         {
            display_name:"",
            seat_id:"",
            student_id:"",
         }

- ## StudentWeb

  ```mermaid
  sequenceDiagram
      participant S as StudentWeb
      participant B as BackendSocket
      participant D as DB
      participant R as Redis
      participant A as TeacherAPP

      S->>B: 1. set_student_name
      B->>D: 2. update display_name in DB student_attend
      B->>R: 3. get teacher sid in Redis
      B->>A: 4. emit  TeacherAPP


  ```
