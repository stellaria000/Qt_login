class AccountDBManagement(BaseDBManagement):
    def __init__(self, db_host, db_port, db_table, db_user, db_pw):
        self.db_host= db_host
        self.db_port= db_port
        self.db_table= db_table
        self.db_user= db_user
        self.db_pw= self.decode_pw(db_pw, db_user)
        self.connectionStatus= None
        try:
            self.engine = create_engine(f"mariadb+mariadbconnector://{self.db_user}:{self.db_pw}@{self.db_host}:{self.db_port}/{self.db_table}")
            Base.metadata.create_all(self.engine)
            self.DBSession = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.connectionStatus = True
        except exc.SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            self.connectionStatus = False
        
    def create(self, dataFrame):
        new_account= AccountDB(id= dataFrame.id,  password= dataFrame.password, 
                                account_package_list= dataFrame.account_package_list, 
                                login_attempt_count= dataFrame.login_attempt_count)

        with self.DBSession() as session:
            try:
                session.add(new_account)
                session.commit()
            except Exception as e:
                print(f"An Error Occurred: {e}")
                session.rollback()
        
    def readAllData(self):
        with self.DBSession() as session:
            dataFrames= session.scalars(select(AccountDB)).all()
            database= {"account": []}
            for account in dataFrames:
                accountEntry= {"id": account.id, "password": account.password, 
                                "account_package_list": account.account_package_list,
                                "login_attempt_count": account.login_attempt_count, 
                                "use_or_not": account.use_or_not}
                database["account"].append(accountEntry)
            return database


    def update(self, idx, dataFrame): # UPDATES DATABASE PACKAGE LIST
        with self.DBSession() as session:
            db_account= session.excute(select(AccountDB).where(AccountDB.id== idx)).scalar_one_or_none()

        if db_account:
            db_account.id= dataFrame.id
            db_account.account_package_list= dataFrame.account_package_list
            
    def delete(self, idx):
        with self.DBSession() as session:
            db_account= session.execute(select(AccountDB).where(AccountDB.id== idx)).scalar_one_or_none()

        if db_account:
            try:
                session.delete(db_account)
                session.commit()
                print("DELETE ACCOUNT DONE")
            except Exception as e:
                session.rollback()
                print(f"An Error Occurred: {e}")

# LOGIN FAILED ATTEMPT COUNTING METHODS
    def updateLoginAttempts(self, id, attempts):
        try: 
            with self.DBSession() as session:
                stmt= update(AccountDB).where(AccountDB.id== id).values(login_attempt_count= attempts)
                session.execute(stmt)
                session.commit()
        except Exception as e: print(f"Error updating login attempts in database: {e}")
    
    def updateUseorNot(self, id, use_or_not):
        try:
            with self.DBSession() as session:
                stmt= update(AccountDB).where(AccountDB.id== id).values(use_or_not= use_or_not)
                session.execute(stmt)
                session.commit()

        except Exception as e: print(f"Error updating USE_OR_NOT in database: {e}")
    
# PASSWORD ENCRYTION& DECRYPTION METHODS
    def generate_salted_hash(self, password, salt_bytes): 
        # FIRST HASH
        sha256_1st= hashlib.sha256()
        sha256_1st.update(password.encode('utf-8'))
        hash_1st= sha256_1st.hexdigest()

        # CONVERT SALT INTO BASE64
        salt= base64.b64encode(salt_bytes).decode('utf-8')

        # SECOND HASH- SHA256(SHA256(PW)+ SALT))
        sha256= hashlib.sha256()
        combined= (hash_1st+ salt).encode('utf-8')  
        sha256.update(combined)
        hash_result= sha256.digest()

        # RETURN THE FINAL RESULT INTO BASE64
        return base64.b64encode(hash_result).decode('utf-8')

    def encrypt_password(self, password, id): 
        # GENERATE SALT BY USING ID
        salt_string= (id[::-1]+ id).lower()
        salt_bytes= salt_string.encode('utf-8')

        # ENCRYPT   
        return self.generate_salted_hash(password, salt_bytes)


class SystemDBManagement(BaseDBManagement):
  def __init__(self, db_host, db_port, db_table, db_user, db_pw):
    self.db_host= db_host
    self.db_port= db_port
    self.db_table= db_table
    self.db_user= db_user
    self.db_pw= self.decode_pw(db_pw, db_user)
    self.connectionStatus= None
    try:
        self.engine = create_engine(f"mariadb+mariadbconnector://{self.db_user}:{self.db_pw}@{self.db_host}:{self.db_port}/{self.db_table}")
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.connectionStatus = True
    except exc.SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")
        self.connectionStatus = False
  
  def create(self, dataFrame): pass

  def readAllData(self):
    with self.DBSession() as session:
      dataFrames= session.scalars(select(SystemDB))
      database= {"system": []}
      for system in dataFrames:
        systemEntry= {"sys_id": system.sys_id, "sys_name": system.sys_name}
        database["system"].append(systemEntry)
      
      return database
  
  def update(self, idx, dataFrame):
    with self.DBSession() as session:
      db_system= session.excute(select(SystemDB).where (SystemDB.sys_id== idx)).scalar_one_or_none()
    if db_system:
      db_system.sys_id= dataFrame.sys_id
      db_system.sys_name= dataFrame.sys_name
  
  def delete(self, idx):
    with self.DBSession() as session:
      db_system= session.exeture(select(SystemDB).where(SystemDB.sys_id== idx)).scalar_one_or_none()

    if db_system:
      try:
        session.delete(db_system)
        session.commit()
        print("DELETE SYSTEM DONE") 
      except Exception as e:
        session.rollback()  
        print(f"An error Occurred: {e}")