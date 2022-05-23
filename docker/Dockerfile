FROM python
WORKDIR /kindle

RUN python -m pip install --upgrade pip
RUN pip3 install requests
RUN pip3 install bs4

COPY . .
CMD [ "python3" , "nhk.py" ]
