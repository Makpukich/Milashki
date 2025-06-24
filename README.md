# Milashki API  
### This is the server part of a web application for managing user subscriptions.

## Technology Stack  
- Python 3.12  
- FastAPI - web framework  
- SQLAlchemy (async) - ORM  
- Uvicorn - ASGI server  
- Pydantic - data validation  
- JWT - authentication  

## Installation  

Clone the repository:  
```bash  
git clone https://github.com/yourusername/milashki-api.git  
cd milashki-api  
```  

Run:  
```bash  
uvicorn main:app --reload  
```  
After launching, the API will be available at: http://localhost:8000  

## All API Endpoints  
### Authentication  
`POST /auth/register` - User registration  

`POST /auth/login` - Login (get JWT)  

`GET /auth/me` - Current user info  

### Account Management  
`GET /accounts/` - List all accounts  

`POST /accounts/` - Create an account  

`GET /accounts/<id>` - Get an account  

`PUT /accounts/<id>` - Update an account  

`DELETE /accounts/<id>` - Delete an account  

### Subscription Management  
`GET /subscriptions/` - List all subscriptions  

`POST /subscriptions/` - Create a subscription  

`GET /subscriptions/<id>` - Get a subscription  

`PUT /subscriptions/<id>` - Update a subscription  

`DELETE /subscriptions/<id>` - Delete a subscription  

### User Subscriptions  
`GET /User_subs/` - All user subscriptions  

`POST /User_subs/` - Add a subscription to a user  

`GET /User_subs/<user_id>/<subscription_id>` - Specific user subscription  

`GET /subscriptions/<user_id>` - Subscriptions of a specific user  

`DELETE /subscriptions/<user_id>/<sub_id>` - Remove a subscription from a user
