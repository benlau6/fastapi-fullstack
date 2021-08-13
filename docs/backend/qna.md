# Q&A

!!! question "app/prestart.sh not found?"
??? solution
    set **git config core.autocrlf false** before using 'git add .' if you are using windows

!!! question "Value of type "Optional[UserInDB]" is not indexable / Incompatible return value type (got "Optional[UserInDB]", expected "UserInDB")?"
??? solution
    assert Object before take attribute!

    