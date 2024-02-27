- # 事件名稱: teacher_force_logout

- ## Request(client emit data):

       {
          user_id:"",
          org_id:"",
       }

- ## CallBackResponse:

      None

- ## Relative Infrastructure

  1. Redis
  2. DB

- ## Usecase

  - ### 1. TeacherHub force logout TeacherAPP user

    - #### Clients:

      1. TeacherHub: 在 Hub 中，選擇一位當前處於「上線狀態」的使用者，並執行操作使該使用者被強制登出。

    - #### Listeners:

      1. TeacherAPP：APP 會接收到被迫登出的通知。接著，APP 將自動進行登出操作。

    - #### Response(Listeners):

      1. TeacherAPP:

         - event_name = 'teacher_force_logout'

           ```
             {"user_id": ""}
           ```

         - broadcast_channel:

           ```
            the sid of the force_logout user
           ```

      - #### FLOW

        ```mermaid
        sequenceDiagram
            participant M as TeacherHub
            participant B as Backend
            participant R as Redis
            participant D as DB
            participant A as TeacherAPP

            M->>B: 1. emit force_logout
            B->>D: 2. query open lesson
            D->>B: get open lesson
            alt If open lesson exists
                  B->>+D: execute end lesson
                  D->>+B: success
            end
            B->>R: 3. set "cooldown:org_{org_id}_user_{user_id}" key & 5 mins TTL
            R->>B: success
            B->>R: 4. query "{user_id}" key to find forced_logout_teacher sid
            R->>B: get forced_logout_teacher sid
            B->>A: 5. emit TeacherAPP(forced_logout_teacher) {"user_id": ""}


        ```
