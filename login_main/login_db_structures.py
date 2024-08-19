class AccountDB(Base):  # LOGIN ACCOUNT TABLE
  __tablename__= "ACCOUNTS"
  id= Column('ID', String(255), primary_key= True, autoincrement= False)
  account_package_list= Column('account_package_list', String(64), nullable= True)
  password= Column('PASSWORD', String(255), nullable= False)


class SystemDB(Base):
  __tablename__= "SYSTEMS"
  sys_id= Column('SYS_ID', Integer, primary_key= True, autoincrement= False)
  sys_name= Column('SYS_NAME', String(255), nullable= False)