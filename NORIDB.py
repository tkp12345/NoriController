import sqlite3

"""
    -모든 select 함수는 return 값이있습니다 
    -setting 테이블이 '커스텀'관련 테이블입니다 
    
"""


## 커스텀 테이블
class Setting:
    conn = sqlite3.connect('DB/testdb4.db')
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')

    ## "+" 버튼이 눌리면 사용되는 로직
       ## id 값(클래스변수)을 설정해 커스텀을 추가한다
    @classmethod
    def insert_Setting(self, id, setting):
        sql = 'insert into setting(id,setting) values(?,?) '
        Setting.cur.execute(sql, (id, setting))
        Setting.conn.commit()

    ## 커스텀이름을 변경하면 사용되는 로직
       ## 커스텀 기존이름 "CUSTOM" => "사용자정의명"
    @classmethod
    def update_Setting_name(self, id, setting):
        sql='update setting set setting=? where id=?'
        Setting.cur.execute(sql, (setting, id))
        Setting.conn.commit()

    @classmethod
    def delete_Setting(self, id):
        Setting.cur.execute('PRAGMA foreign_keys = ON')
        sql = 'delete from setting where id=?'
        Setting.cur.execute(sql, (id,))
        Setting.conn.commit()

    def select_Setting(self):
        sql = "select * from setting"
        Setting.cur.execute(sql)
        rs = Setting.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

#즐겨찾기 테이블
class Favorites:
    conn = sqlite3.connect('DB/testdb4.db')
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')

    @classmethod
    def insert_Favorites(self, eno):
        sql = 'insert into favorites(eno) values(?)'
        Favorites.cur.execute(sql, (eno,))
        Favorites.conn.commit()

    @classmethod
    def delete_Favorites(self, eno):
        sql = 'delete from favorites where eno=?'
        Favorites.cur.execute(sql, (eno,))
        Favorites.conn.commit()

    @classmethod
    def select_Favorites(self):
        sql = "select * from favorites"
        Favorites.cur.execute(sql)
        rs = Favorites.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list


#버튼 테이블
class ButtonDB:
    conn = sqlite3.connect('DB/testdb4.db')
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')

    @classmethod
    def insert_Button(self, eno, buttonA, buttonB, buttonX, buttonY):
        Setting.cur.execute('PRAGMA foreign_keys = ON')
        sql ="insert into button(eno,buttonA,buttonB,buttonX,buttonY) values(?,?,?,?,?)"
        ButtonDB.cur.execute(sql,(eno,buttonA,buttonB,buttonX,buttonY))
        ButtonDB.conn.commit()

## 버튼 조회
    @classmethod
    def select_ButtonA(self,eno):
        sql ="select * from button where eno=?"
        ButtonDB.cur.execute(sql,(eno,))
        rs = ButtonDB.cur.fetchall()
        x = rs[0][1]
        return x

    @classmethod
    def select_ButtonB(self, eno):
        sql = "select * from button where eno=?"
        ButtonDB.cur.execute(sql, (eno,))
        rs = ButtonDB.cur.fetchall()
        x = rs[0][2]
        return x

    @classmethod
    def select_ButtonX(self, eno):
        sql = "select * from button where eno=?"
        ButtonDB.cur.execute(sql, (eno,))
        rs = ButtonDB.cur.fetchall()
        x = rs[0][3]
        return x

    @classmethod
    def select_ButtonY(self, eno):
        sql = "select * from button where eno=?"
        ButtonDB.cur.execute(sql, (eno,))
        rs = ButtonDB.cur.fetchall()
        x = rs[0][4]
        return x

    @classmethod
    def select_Button(self):
        sql = "select * from Button"
        ButtonDB.cur.execute(sql)
        rs = ButtonDB.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

## 버튼 수정
    @classmethod
    def update_ButtonA(self,eno,buttonA):
        sql = "update button set buttonA=? where eno=?"
        ButtonDB.cur.execute(sql, (buttonA, eno))
        ButtonDB.conn.commit()


    @classmethod
    def update_ButtonB(self, eno, buttonB):
        sql = "update button set buttonB=? where eno=?"
        ButtonDB.cur.execute(sql, (buttonB, eno))
        ButtonDB.conn.commit()


    @classmethod
    def update_ButtonX(self, eno, buttonX):
        sql = "update button set buttonX=? where eno=?"
        ButtonDB.cur.execute(sql, (buttonX, eno))
        ButtonDB.conn.commit()


    @classmethod
    def update_ButtonY(self, eno, buttonY):
        sql = "update button set buttonY=? where eno=?"
        ButtonDB.cur.execute(sql, (buttonY, eno))
        ButtonDB.conn.commit()

##버튼 삭제

    @classmethod
    def delete_Button(self, eno):
        sql = "delete from button where eno=?"
        ButtonDB.cur.execute(sql, (eno,))
        ButtonDB.conn.commit()


class PitchDB:
    conn = sqlite3.connect('DB/testdb4.db')
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')

##pitch 추가
    @classmethod
    def insert_Pitch(self,eno, pitch_ID, pitch_min, pitch_max, pitch_input):
        sql = "insert into pitch(eno, pitch_ID, pitch_min, pitch_max, pitch_input) values(?,?,?,?,?)"
        PitchDB.cur.execute(sql, (eno, pitch_ID, pitch_min, pitch_max, pitch_input))
        PitchDB.conn.commit()

    @classmethod
    def delete_Pitch(self, eno, pitch_ID):
        sql = "delete from pitch where eno=? and pitch_ID=?"
        PitchDB.cur.execute(sql, (eno, pitch_ID))
        PitchDB.conn.commit()

## pitch 조회 (매개변수 : eno ,pitch_id)
    @classmethod
    def select_Pitch_eno(self, eno):
        sql = "select * from pitch where eno=?"
        PitchDB.cur.execute(sql, (eno,))
        rs = PitchDB.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

    @classmethod
    def select_Pitch(self):
        sql = "select * from pitch"
        PitchDB.cur.execute(sql)
        rs = PitchDB.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list


##pitch 수정  매개변수로 받은값으로 데이터를 수정합니다
    @classmethod
    def update_Pitch_min(self, eno, pitch_ID, pitch_min):
        sql = "update pitch set pitch_min=? where eno=? and pitch_ID=?"
        PitchDB.cur.execute(sql, (pitch_min, eno, pitch_ID))
        PitchDB.conn.commit()

    @classmethod
    def update_Pitch_max(self, eno, pitch_ID, pitch_max):
        sql = "update pitch set pitch_max=? where eno=? and pitch_ID=?"
        PitchDB.cur.execute(sql, (pitch_max, eno, pitch_ID))
        PitchDB.conn.commit()

    @classmethod
    def update_Pitch_input(self, eno, pitch_ID, pitch_input):
        sql = "update pitch set pitch_input=? where eno=? and pitch_ID=?"
        PitchDB.cur.execute(sql, (pitch_input, eno, pitch_ID))
        PitchDB.conn.commit()


class RollDB:
    conn = sqlite3.connect('DB/testdb4.db')
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')


## roll 추가
    @classmethod
    def insert_Roll(self, eno, roll_ID, roll_min, roll_max, roll_input):
        sql = "insert into roll(eno, roll_ID, roll_min, roll_max, roll_input) values(?,?,?,?,?)"
        RollDB.cur.execute(sql, (eno, roll_ID, roll_min, roll_max, roll_input))
        RollDB.conn.commit()

    @classmethod
    def delete_Roll(self, eno, roll_ID):
        sql = "delete from roll where eno=? and roll_ID=?"
        RollDB.cur.execute(sql, (eno, roll_ID))
        RollDB.conn.commit()

    def select_Roll_eno(eno):
        sql = "select * from roll where eno=?"
        RollDB.cur.execute(sql, (eno,))
        rs = RollDB.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

    @classmethod
    def select_Roll(self):
        sql = "select * from roll"
        RollDB.cur.execute(sql)
        rs = RollDB.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

## roll 수정
    @classmethod
    def update_Roll_min(self, eno, roll_ID, roll_min):
        sql = "update roll set roll_min=? where eno=? and roll_ID=?"
        RollDB.cur.execute(sql, (roll_min, eno, roll_ID))
        RollDB.conn.commit()

    @classmethod
    def update_Roll_max(self, eno, roll_ID, roll_max):
        sql = "update roll set roll_max=? where eno=? and roll_ID=?"
        RollDB.cur.execute(sql, (roll_max, eno, roll_ID))
        RollDB.conn.commit()

    @classmethod
    def update_Roll_input(self, eno, roll_ID, roll_input):
        sql = "update roll set roll_input=? where eno=? and roll_ID=?"
        RollDB.cur.execute(sql, (roll_input, eno, roll_ID))
        RollDB.conn.commit()

class YawDB:
    conn = sqlite3.connect('DB/testdb4.db')
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')

## yaw 추가
    @classmethod
    def insert_Yaw(self, eno, yaw_ID, yaw_min, yaw_max, yaw_input):
        sql = "insert into yaw(eno, yaw_ID, yaw_min, yaw_max, yaw_input) values(?,?,?,?,?)"
        YawDB.cur.execute(sql, (eno, yaw_ID, yaw_min, yaw_max, yaw_input))
        YawDB.conn.commit()

    @classmethod
    def delete_Yaw(self, eno, yaw_ID):
        sql = "delete from yaw where eno=? and yaw_ID=?"
        YawDB.cur.execute(sql, (eno, yaw_ID))
        YawDB.conn.commit()

    ## yaw 조회
    def select_Yaw_eno(eno):
        sql = "select * from yaw where eno=?"
        YawDB.cur.execute(sql, (eno,))
        rs = YawDB.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

    @classmethod
    def select_Yaw(self):
        sql = "select * from yaw"
        YawDB.cur.execute(sql)
        rs = YawDB.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

## yaw 수정
    @classmethod
    def update_Yaw_min(self, eno, yaw_ID, yaw_min):
        sql = "update yaw set yaw_min=? where eno=? and yaw_ID=?"
        YawDB.cur.execute(sql, (yaw_min, eno, yaw_ID))
        YawDB.conn.commit()

    @classmethod
    def update_Yaw_max(self, eno, yaw_ID, yaw_max):
        sql = "update yaw set yaw_max=? where eno=? and yaw_ID=?"
        YawDB.cur.execute(sql, (yaw_max, eno, yaw_ID))
        YawDB.conn.commit()

    @classmethod
    def update_Yaw_input(self, eno, yaw_ID, yaw_input):
        sql = "update yaw set yaw_input=? where eno=? and yaw_ID=?"
        YawDB.cur.execute(sql, (yaw_input, eno, yaw_ID))
        YawDB.conn.commit()

class Camera:
    conn = sqlite3.connect('DB/testdb4.db')
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')


# 카메라 입력
    @classmethod
    def insert_Camera(self, eno, camera_ID, begin_x, begin_y, end_x, end_y, camera_input):
        sql = "insert into camera(eno, camera_ID, begin_x, begin_y, end_x, end_y, camera_input) values(?,?,?,?,?,?,?)"
        Camera.cur.execute(sql, (eno, camera_ID, begin_x, begin_y, end_x, end_y, camera_input))
        Camera.conn.commit()



## 카메라화면 사각형 마우스 드래그 이벤트함수

    ## 마우스 눌릴때 (begin_x, begin_y) 가져옴
    @classmethod
    def insert_Camera_mouseDown(self,eno,begin_x,begin_y):
        sql = "insert into camera(eno, begin_x, begin_y, end_x, end_y, camera_input) values(?,?,?,?,?,?)"
        Camera.cur.execute(sql, (eno, begin_x, begin_y, 0, 0, 0))

    ## 마우스 땔때 (end_x, begin_y) 값으로 기존데이터 수정
    @classmethod
    def update_Camera_mouseUP(self,eno,end_x,end_y):
        sql = "update camera set end_x=?,end_y=? where eno=?"
        Camera.cur.execute(sql, (end_x,end_y,eno))
        Camera.conn.commit()


##카메라 조회
    @classmethod
    def select_Begin_x(self, eno):
        sql = "select * from camera where eno=?"
        Camera.cur.execute(sql, (eno,))
        rs = Camera.cur.fetchall()  # [(eno, begin_x, begin_y, end_x, end_y, camera_input)]
        x = rs[0][1]  # camera_input 칼럼 데이터
        return x

    @classmethod
    def select_Begin_y(self, eno):
        sql = "select * from camera where eno=?"
        Camera.cur.execute(sql, (eno,))
        rs = Camera.cur.fetchall()
        x = rs[0][2]
        return x

    @classmethod
    def select_End_x(self, eno):
        sql = "select * from camera where eno=?"
        Camera.cur.execute(sql, (eno,))
        rs = Camera.cur.fetchall()
        x = rs[0][3]
        return x

    @classmethod
    def select_End_y(self, eno):
        sql = "select * from camera where eno=?"
        Camera.cur.execute(sql, (eno,))
        rs = Camera.cur.fetchall()
        x = rs[0][4]
        return x


    @classmethod
    def select_Camera_input(self, eno):
        sql = "select * from camera where eno=?"
        Camera.cur.execute(sql, (eno,))
        rs = Camera.cur.fetchall()
        x= rs[0][5]
        return x

    @classmethod
    def select_Camera(self):
        sql = "select * from camera"
        Camera.cur.execute(sql)
        rs = Camera.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

    @classmethod
    def select_Camera_eno(self, eno):
        sql = "select * from camera where eno=?"
        Camera.cur.execute(sql, (eno,))
        rs = Camera.cur.fetchall()
        list = []
        for i in rs:
            list.append(i)
        return list

##카메라 수정
    @classmethod
    def update_Begin_x(self, eno, begin_x):
        sql = "update camera set begin_x=? where eno=?"
        Camera.cur.execute(sql, (begin_x,eno))
        Camera.conn.commit()

    @classmethod
    def update_Begin_y(self, eno, begin_y):
        sql = "update camera set begin_y=? where eno=?"
        Camera.cur.execute(sql, (begin_y, eno))
        Camera.conn.commit()

    @classmethod
    def update_End_x(self, eno, end_x):
        sql = "update camera set end_x=? where eno=?"
        Camera.cur.execute(sql, (end_x, eno))
        Camera.conn.commit()

    @classmethod
    def update_End_y(self, eno, end_y):
        sql = "update camera set end_y=? where eno=?"
        Camera.cur.execute(sql, (end_y, eno))
        Camera.conn.commit()

    @classmethod
    def update_Camera_input(self, eno, camera_ID, camera_input):
        sql = "update camera set camera_input=? where eno=? and camera_ID=?"
        Camera.cur.execute(sql, (camera_input, eno, camera_ID))
        Camera.conn.commit()

    @classmethod
    def delete_Camera(self,eno, camera_ID):
        sql ="delete from camera where eno=? and camera_ID=?"
        Camera.cur.execute(sql, (eno, camera_ID))
        Camera.conn.commit()
        

#테이블 생성
class DB:
    conn = sqlite3.connect('DB/noridb.db')
    cur = conn.cursor()

    @classmethod
    def create_setting(self):
        DB.cur.execute('''
            create table setting(
                id integer PRIMARY KEY,
                setting text
                );
                ''')
        DB.conn.commit()

    @classmethod
    def create_button(self):
        DB.cur.execute('''
            create table button(
                eno integer PRIMARY KEY,
                buttonA text,
                buttonB text,
                buttonX text,
                buttonY text,
                FOREIGN KEY (eno) REFERENCES setting(id) on delete cascade
                );
                ''')
        DB.conn.commit()

    @classmethod
    def create_camera(self):
        DB.cur.execute('''
            create table camera(
                eno integer,
                camera_ID integer,
                begin_x integer,
                begin_y integer,
                end_x integer,
                end_y integer,
                camera_input text,
                
                primary key(eno, camera_ID),          
                FOREIGN KEY (eno) REFERENCES setting(id) on delete cascade
                );
                ''')
        DB.conn.commit()

    @classmethod
    def create_favorites(self):
        DB.cur.execute('''
            create table favorites(
                eno integer PRIMARY KEY,
                FOREIGN KEY (eno) REFERENCES setting(id) on delete cascade
                );
                ''')
        DB.conn.commit()

    @classmethod
    def create_pitch(self):
        DB.cur.execute('''
            create table pitch(
                eno integer,
                pitch_ID integer ,
                pitch_min integer,
                pitch_max integer,
                pitch_input text,
                primary key(eno,pitch_ID),
                FOREIGN KEY (eno) REFERENCES setting(id) on delete cascade
                );
                ''')
        DB.conn.commit()

    @classmethod
    def create_roll(self):
        DB.cur.execute('''
            create table roll(
                eno integer ,
                roll_ID integer,
                roll_min integer,
                roll_max integer,
                roll_input text,
                primary key(eno,roll_ID),
                FOREIGN KEY (eno) REFERENCES setting(id) on delete cascade
                );
                ''')
        DB.conn.commit()

    @classmethod
    def create_yaw(self):
        DB.cur.execute('''
            create table yaw(
                eno integer ,
                yaw_ID integer,
                yaw_min integer,
                yaw_max integer,
                yaw_input text,
                primary key(eno,yaw_ID),
                FOREIGN KEY (eno) REFERENCES setting(id) on delete cascade
                );
                ''')
        DB.conn.commit()



if __name__=="__main__" :
    pass
    #list = RollDB.select_Roll_eno(self=None, eno=0)
    #print(list)
    #print(list[1][4].lower())

    #conn = sqlite3.connect('DB/noridb.db')
    #DB.create_setting()
    #DB.create_button()
    #DB.create_camera()
    #DB.create_yaw()
    #DB.create_pitch()
    #DB.create_roll()
    #DB.create_favorites()


    #Favorites.insert_Favorites(0)

    #Camera.insert_Camera(0, 2, 200, 200, 500, 500, 'eee')
