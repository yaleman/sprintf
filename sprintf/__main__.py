""" CLI version """

import uvicorn # type: ignore

if __name__ == '__main__':
    uvicorn.run(app="sprintf:app", reload=True)
