from datetime import datetime, date, time
from abc import ABC, abstractmethod

from enum import Enum

############################################
# Definition of Enumerations
############################################

class ContactM(Enum):
    EMAIL = "EMAIL"
    TELEPHONE = "TELEPHONE"
    LETTER = "LETTER"


############################################
# Definition of Classes
############################################

class Platform(ABC):

    pass
class Author:

    def __init__(self, name: str, email: str, Book: set["Book"] = None):
        self.name = name
        self.email = email
        self.Book = Book if Book is not None else set()
        
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = email

    @property
    def Book(self):
        return self.__Book

    @Book.setter
    def Book(self, value):
        # Bidirectional consistency
        old_value = getattr(self, f"_Author__Book", None)
        self.__Book = value if value is not None else set()
        
        # Remove self from old opposite end
        if old_value is not None:
            for item in old_value:
                if hasattr(item, "Author"):
                    opp_val = getattr(item, "Author", None)
                    
                    if isinstance(opp_val, set):
                        opp_val.discard(self)
                    
        # Add self to new opposite end
        if value is not None:
            for item in value:
                if hasattr(item, "Author"):
                    opp_val = getattr(item, "Author", None)
                    
                    if opp_val is None:
                        setattr(item, "Author", set([self]))
                    elif isinstance(opp_val, set):
                        opp_val.add(self)
                    

    @abstractmethod
    def func(self) -> str:
        pass

    def notify(self, sms: str = "message", contact_method: ContactM):
        # TODO: Implement notify method
        pass

class Book:

    def __init__(self, tittle: str, pages: int, edition: date, Author: set["Author"] = None, Library: "Library" = None):
        self.tittle = tittle
        self.pages = pages
        self.edition = edition
        self.Author = Author if Author is not None else set()
        self.Library = Library
        
    @property
    def edition(self) -> date:
        return self.__edition

    @edition.setter
    def edition(self, edition: date):
        self.__edition = edition

    @property
    def pages(self) -> int:
        return self.__pages

    @pages.setter
    def pages(self, pages: int):
        self.__pages = pages

    @property
    def tittle(self) -> str:
        return self.__tittle

    @tittle.setter
    def tittle(self, tittle: str):
        self.__tittle = tittle

    @property
    def Library(self):
        return self.__Library

    @Library.setter
    def Library(self, value):
        # Bidirectional consistency
        old_value = getattr(self, f"_Book__Library", None)
        self.__Library = value
        
        # Remove self from old opposite end
        if old_value is not None:
            if hasattr(old_value, "Book"):
                opp_val = getattr(old_value, "Book", None)
                if opp_val == self:
                    setattr(old_value, "Book", None)
                
        # Add self to new opposite end
        if value is not None:
            if hasattr(value, "Book"):
                opp_val = getattr(value, "Book", None)
                setattr(value, "Book", self)

    @property
    def Author(self):
        return self.__Author

    @Author.setter
    def Author(self, value):
        # Bidirectional consistency
        old_value = getattr(self, f"_Book__Author", None)
        self.__Author = value if value is not None else set()
        
        # Remove self from old opposite end
        if old_value is not None:
            for item in old_value:
                if hasattr(item, "Book"):
                    opp_val = getattr(item, "Book", None)
                    
                    if isinstance(opp_val, set):
                        opp_val.discard(self)
                    
        # Add self to new opposite end
        if value is not None:
            for item in value:
                if hasattr(item, "Book"):
                    opp_val = getattr(item, "Book", None)
                    
                    if opp_val is None:
                        setattr(item, "Book", set([self]))
                    elif isinstance(opp_val, set):
                        opp_val.add(self)
                    

class Literature(Book):

    def __init__(self, tittle: str, pages: int, edition: date, Library: "Library", Author: set["Author"] = None):
        super().__init__(tittle, pages, edition, Library, Author)
        
class Fantasy(Book):

    def __init__(self, tittle: str, pages: int, edition: date, Library: "Library", Author: set["Author"] = None):
        super().__init__(tittle, pages, edition, Library, Author)
        
class Science(Book):

    def __init__(self, tittle: str, pages: int, edition: date, Library: "Library", Author: set["Author"] = None):
        super().__init__(tittle, pages, edition, Library, Author)
        
class Library:

    def __init__(self, name: str, address: str, Book: "Book" = None):
        self.name = name
        self.address = address
        self.Book = Book
        
    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, address: str):
        self.__address = address

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def Book(self):
        return self.__Book

    @Book.setter
    def Book(self, value):
        # Bidirectional consistency
        old_value = getattr(self, f"_Library__Book", None)
        self.__Book = value
        
        # Remove self from old opposite end
        if old_value is not None:
            if hasattr(old_value, "Library"):
                opp_val = getattr(old_value, "Library", None)
                if opp_val == self:
                    setattr(old_value, "Library", None)
                
        # Add self to new opposite end
        if value is not None:
            if hasattr(value, "Library"):
                opp_val = getattr(value, "Library", None)
                setattr(value, "Library", self)
