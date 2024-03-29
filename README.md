<h1 align="center" id="title">Grocery Store</h1>

<p align="center"><img src="https://socialify.git.ci/vinay02yadav/Grocery-Store/image?font=KoHo&amp;language=1&amp;name=1&amp;owner=1&amp;stargazers=1&amp;theme=Dark" alt="project-image"></p>

<p id="description">This project is a platform for selling grocery items where users can register login buy and search for different products and categories using their names or price range. Manager and admin can create and manage category and products.</p>

<h2>🚀 Demo</h2>

[https://drive.google.com/file/d/1pJ5UlyDxUD9tStSfQC1vjvgam1F7IHY0/view?usp=sharing](https://drive.google.com/file/d/1pJ5UlyDxUD9tStSfQC1vjvgam1F7IHY0/view?usp=sharing)

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   User and Manager registration using JWT (token-based authentication)
* What User can do : 
     * Ability to buy multiple products from one or multiple sections.
     * Ability to search multiple products or categories based on their name or price.
     * Ability to see out of stock products that are not available.
     * Ability to see the total amount to be paid for the transaction.
     * Cart button updates Dynamically.
* What Manager can do :
     * Ability to add, edit and delete Category from the Shop with Admin's permission
     * Ability to add, edit and delete Items from the shop
* What Admin can do :
     * Accepts or deny the request from Manager.
     * Accepts or deny the new Manager joining request.
     * Gets the shop's monthly report.
* Backend Jobs :
     * Scheduled Jobs : Send monthly progress report using mail to the User.
     * Daily Reminder Jobs : Receive daily reminders to the Users.
     * User Triggered Async Job: Export blog details as CSV.
* Performance and Caching

<h2>🛠️ Installation Steps:</h2>

<p>1. Start redis-server and redis-cli in windows.</p>

<p>2. Open backend directory</p>

```
cd backend
```

<p>3. Open new terminal and run this command to start backend server.</p>

```
python main.py
```

<p>4. Open new terminal to start celery worker.</p>

```
celery -A main.celery worker --pool=solo -l info
```

<p>5. Open new terminal to start celery beat.</p>

```
celery -A main.celery beat --max-interval 600 -l info
```

<p>6. Navigate to the frontend folder.</p>

```
cd ../frontend
```

<p>7. Open terminal here to install relevant packages</p>

```
npm install
```

<p>8. Open terminal here to start frontend server.</p>

```
npm run serve
```

<p>9. You are ready to ROCK now !!</p>
