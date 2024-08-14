class LoginDB_management(BaseDBManagement):
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
    new_account= AccountDB(id= dataFrame.id, sys_id= dataFrame.sys_id, password= dataFrame.password)
    with self.DBSession() as session:
      try:
        session.add(new_account)
        session.commit()
      except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        
  def readAllData(self): # ???
    with self.DBSession() as session:
      dataFrames= session.scalars(select(AccountDB)) 
      database= {"account": []}
      for account in dataFrames:
        accountEntry= {"id": account.id, "sys_id": account.sys_id, "password": account.password}
        database["account"].append(accountEntry)
      return database
    
    
  def update(self, idx, dataFrame):
    with self.DBSession() as session:
        db_account= session.excute(select(AccountDB).where(AccountDB.id== idx)).scalar_one_or_none()
    
    if db_account:
      db_account.id= dataFrame.id
      db_account.sys_id= dataFrame.sys_id
      
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
        print(f"An error Occurred: {e}")

class SystemDB_management(BaseDBManagement):
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

  def realAllData(self):
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
# login DB structures

class AccountDB(Base):
  __tablename__= "ACCOUNTS"
  id= Column('ID', String(255), primary_key= True, autoincrement= False)
  sys_id= Column('SYS_ID', Integer, nullable= False)
  password= Column('PASSWORD', Integer, nullable= False)
  
class SystemDB(Base):
  __tablename__= "SYSTEMS"
  sys_id= Column('SYS_ID', Integer, primary_key= True, autoincrement= True)
  sys_name= Column('SYS_NAME', String(255), nullable= False)