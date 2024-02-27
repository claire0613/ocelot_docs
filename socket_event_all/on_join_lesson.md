- # 事件名稱: join_lesson

- ### Request(client emit data):

  ```
  {
    user_id:str,
    lesson_id:str,
    access_token:str,
    role:str,
  }
  ```

- ## Relative Infrastructure

  1. Redis
  2. DB

- ### CallBackResponse:

  ```
  {"status": SUCCESS|ERROR, "data": {}}
  ```

- ## Usecase

  - ### 1. TeacherAPP Join Lesson

    - #### Clients:

      1. TeacherAPP: TeacherAPP join lesson 訂閱 lesson_id channel

    - #### Listeners:

          None

    - #### Response(Listeners):

          None

      - #### FLOW

        ```mermaid
        sequenceDiagram

            participant A as TeacherAPP
            participant B as Backend
            participant R as Redis
            participant D as DB

            A->>B: 1. join_lesson
            B->>D: 2. check_lesson_exists
            alt if not lesson exists
              D->>B: not found lesson_id
              B->>A: return error
            else lesson exists
               D->>B: success

            end
            B->>B: 3. enter_room
            B->>D: 4. query student_attend seat by lesson_id nad student_id
            D->>B : get seat
            B->>B : get session
            alt if seat
                B->>B: update session {seat:'seat}
            end
            B->>B: save session
            B->>R: 5. query "lesson_seat_{lesson_id}"key
            R->>B : get lesson_seat_in_redis
            alt if not lesson_seat_* exists
                B->>R: add "lesson_seat_*" key  {1:"",2:""....}
                R->>B: return
            end
            B->>R: add lesson_teacher_{lesson_id}"key {{user_id}:sid} & TTL 24hrs
            R->>B: return
            B->>R: set user_id key {"lesson_id": lesson_id}
            R->>B: return
            B->>A: return success

        ```

  - ### 2. ParticipantWeb Join Lesson

    - #### Clients:

      1.  ParticipantWeb : ParticipantWeb join lesson 訂閱 lesson_id channel

    - #### Listeners:

          None

    - #### Response(Listeners):

          None

    - #### FLOW

      ```mermaid
      sequenceDiagram

          participant A as TeacherAPP
          participant B as Backend
          participant R as Redis
          participant D as DB

          A->>B: 1. join_lesson
          B->>D: 2. check_lesson_exists
          alt if not lesson exists
            D->>B: not found lesson_id
            B->>A: return error
          else lesson exists
             D->>B: success

          end
          B->>B: 3. enter_room
          B->>D: 4. query student_attend seat by lesson_id nad student_id
          D->>B : get seat
          B->>B : get session
          alt if seat
              B->>B: update session {seat:'seat}
          end
          B->>B: save session
          B->>R: 5. query "lesson_seat_{lesson_id}"key
          R->>B : get lesson_seat_in_redis
          alt if not lesson_seat_* exists
              B->>R: add "lesson_seat_*" key  {1:"",2:""....}
              R->>B: return
          end
          alt if access_token is not None
              B->>B: get client_id by access_token
              B->>B: save session {"client_id":str,"role":str}
              B->>R: save session get {client_id} key exists
            alt if {client_id} key exists
                B->>B: call mixpanel reconnect
            end
            B->>R: reset sid in  client_id key {"sid":str,"client_id":str,"role":str} & TTL 24 hr
            R->>B: return
            B->>R: reset sid in lesson_student_{lesson_id}  {"client_id":sid}
            R->>B: return
          end

          B->>A: return success

      ```
