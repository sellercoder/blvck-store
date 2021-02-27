from aiogram.dispatcher.filters.state import StatesGroup, State

class DeleteCoupon(StatesGroup):
    Id = State()

class ActivateCoupon(StatesGroup):
    Uid = State()

class NewCoupon(StatesGroup):
    Uid = State()
    Amount = State()
    Confirm = State()

class NewCategory(StatesGroup):
    Name = State()
    Description = State()
    Confirm = State()

class ChangeCategory(StatesGroup):
    Id = State()
    Name = State()
    Description = State()
    Confirm = State()

class DeleteCategory(StatesGroup):
    Id = State()
    Confirm = State()
    
class NewPosition(StatesGroup):
    CategoryID = State()
    Reusable = State()
    Name = State()
    Description = State()
    Price = State()
    Confirm = State()

class ChangePosition(StatesGroup):
    Id = State()
    CategoryID = State()
    Name = State()
    Description = State()
    Price = State()
    Confirm = State()

class DeletePosition(StatesGroup):
    Id = State()
    Confirm = State()
 
class NewItem(StatesGroup):
    PositionID = State()
    IsText = State()
    UploadFile = State()
    SendText = State()
    Reusable = State()
    Confirm = State()

class ManyItems(StatesGroup):
    PositionID = State()
    SetLines = State()
    Confirm = State()


class DeleteItem(StatesGroup):
    Id = State()
    Confirm = State()

class SetToken(StatesGroup):
    set_phone = State()
    set_token = State()

class Cms(StatesGroup):
    set_home = State()
    set_catalog = State()
    set_about = State()

class QiwiBill(StatesGroup):
    get_url = State()






