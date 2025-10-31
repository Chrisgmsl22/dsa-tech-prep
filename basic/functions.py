## these are defined using the def keyword

def greet(name: str) -> None:
    """
        This functionn greets the person passed in as a parameter.
    """
    print(f"Hello: {name}")
    
greet('Alice')

def show_example() -> None:
    """This is called docstring"""
    
def show_various_parameters(name: str, lastName:str) -> str:
    return f'hello {name}{lastName}'

output = show_various_parameters(name='John', lastName='Mikey')
print(output)