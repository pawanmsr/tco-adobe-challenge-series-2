# Topcoder - Adobe Challenge Series

Adobe challenge series on topcoder.  

In this challenge, you will build a simple platform (web app) that allows two firms to sign an agreement by leveraging Adobe Sign API.  

1. Login Screen  
You can create a mock login screen to ask the user to enter the email that they use to register the Adobe Sign API.  
After the user logged in, they will be directed to the dashboard screen.  

2. Dashboard Screen  
On the dashboard screen, there is a PDF document, the firm user can operate the document using PDF tools API.  
The operations should include:  
    - [x] Merge two or more PDFs into a single PDF document.  
    - [x] Split a PDF into two PDF documents, a PDF document should contain at least 1 page. For example, suppose a PDF contains 10 pages, it can be splitted into a PDF with 1 page and the other PDF with 9 pages.  
    - [x] Delete a specific page.  
    - [x] Reorder the pages of a PDF document.  
    - [ ] The firm users can also sign the document using Adobe E-signature. Once any firm user signs the document, the document cannot be operated. If both firm users signed, show a note that the document has already been signed.  

## Structure

The entire application comprises of two smaller applications. The **web** component maintains the system state in a database, serves static web pages for interface, and displays files. The **api** component handles the pdf operations.  

## Requirements

The requirements for **web** component and **api** components need to be installed seperately.  

### WEB Requirements

Please view the **requirements.txt** and **requirements_conda.txt** before installing requirements. Requirements maybe installed using *pip* or any other python package management tool such as [conda](https://docs.conda.io/en/latest/miniconda.html). It is recommended that all requirements be installed in a new python environment. The environment used to generate the **requirements** used multiple channels. You may have to update the channels or download few packages manually.  

### API Requirements

Please view the **package.json** before installing requirements.  

1. Open a new terminal and navigate to project root.  
2. Enter the following commands successively:  
    
    ```shell
    cd api
    npm install
    ```
You will need *npm* to install *node* packages.  

## Configuration

Configurations and credentials need to be added seperately to **web** and **api**.  

### API Configuration

API credentials and logging configuration needs to be specified. Follow [Getting Credentials](https://opensource.adobe.com/pdftools-sdk-docs/release/latest/index.html#getcred) to download a samples directory. This will contain **pdftools-api-credentials.json** file and a **private.key** file. Save these files as is in the **api** directory. The samples directory will also contain a **config** sub directory. Copy this directory with all its content into the **api** directory. The final structure of **api** directory will look similar to this:  

```lang-none
+ repository root  
|   + api  
|   |   + bin  
|   |   |   + www  
|   |   |   + js  
|   |   + config  
|   |   |   - pdftools-sdk-log4js-config.json  
|   |   + public  
|   |   |   - static assets
|   |   + routes
|   |   |   - router modules
|   |   + views  
|   |   - app.js  
|   |   - pdftools-api-credentials.json  
|   |   - package.json  
|   |   - private.key  
|   |   - other files and directories
```

### WEB Configuration

The following files need to be populated with configuration variables and environment variables:  

- app.ini  
- .env

They need to be generated first by copying their respective example files:  

```shell
cd web
cp example.app.ini app.ini
cp example.env .env
```

Here is a guide to various environment variables:  

- *SQLALCHEMY_DATABASE_URI* in **.env** must point to the database and contain the driver. For example, if **MySQL** is used for database hosting and the connection is driven by **PyMySQL** (a python package) then *SQLALCHEMY_DATABASE_URI* will be populated with *mysql+pymysql://user:pass@localhost/database*, where *user*, *pass* and *database* need to be replaced with respective credentials. See [Database](#database) section for more details.  
- *STORAGE_PATH* in **.env** is absolute path to a directory that can be accessed by the application. It is recommended to create a new empty directory in the host system and supply it's path here. Use `pwd` command to know the path of the directory.  
- *EMBED_API_ID* in **.env** provide the client id for the [Adobe PDF Embed API](https://www.adobe.io/apis/documentcloud/dcsdk/pdf-embed.html). This is used to render embeded pdf on web.  
- *API ENDPOINTS* contains the *MERGE*, *SPLIT*, *DELTE*, *REORDER* and *SIGN* fields. Populate them with the respective endpoints from the **api** component. By default the **api** will be hosted at post 3000. See the [**api** configuration](#api-configuration) section to know more.  
- *BASE_URL* in **.env** must remain blank and it must be populated only if the application on hosted server is unable to form web routes correctly.  
- *chdir* in **app.ini** is absolute path of the **web** component of the application in the host system.  
- *virtualenv* in **app.ini** is absolute path to the python environment.  
- Rest of the configuration may be left as is in the respective example files, depending on the host system. Refer [uwsgi configuration](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html) for help in populating **app.ini**.  

The final structure of the web directory will look like this:  

```lang-none
+ repository root  
|   + web  
|   |   + Application  
|   |   |   + static  
|   |   |   + templates   
|   |   |   - __init__.py
|   |   |   - auth.py
|   |   |   - dashboard.py
|   |   |   - forms.py
|   |   |   - models.py
|   |   + Migrations
|   |   |   - database migration files
|   |   - .env  
|   |   - example.env  
|   |   - app.ini  
|   |   - example.app.ini  
|   |   - config.py  
|   |   - start.sh  
|   |   - other files and directories
```

## Database

Create an empty database. If your are using **MySQL** for database hosting, login to mysql and enter the following sql commands to create a database named *acs*.  

```sql
CREATE DATABASE acs;
USE acs;
```

A new database will not contain any tables. You will need to migrate tables to the database (see below).  

### Migration
The application is shipped with in-built migration scripts. Migration scripts migrate tables to the database. Make sure you have [configured](#web-configuration) the **web** component before running the migration. To run table migration, activate the python environment that statisfies all [requirements](#web-requirements), navigate to the application root and enter the following:  

```shell
cd web
flask db upgrade --directory Migrations
```

Verify that tables have been migrated by logging into mysql database.  

```sql
SHOW TABLES;
SELECT * FROM `user`;
SELECT * FROM `file_detail`;
```

Initially the `SELECT` commands will output empty sets. They will be populated as the application is used.  

## Set Up

1. Clone repository.  
2. Install requirements. See [Requirements](#requirements) section.  
3. Setup database. See [Database](#database) section.  
4. Populate configuration files. See [Configuration](#configuration) section.  
5. Migrate database. See [Database Migration](#migration) section.  
6. Start the **web** component.  
    
    ```shell
    cd web
    bash start.sh
    ```

7. Start the **api** component.  
    
    ```shell
    cd api
    npm start
    ```

The start commands must be executed in seperate command line instances.  

## Operations

- Upload  
Upload pdf.
- View  
View uploaded pdfs and pdfs generated as result of various other operations.  
- Merge  
Merge two pdfs.
- Reorder  
Reorder the pdf pages.  
- Delete  
Delete a page from pdf.  
- Split  
Split pdf into multiple files.  
This operation was under development when video demonstration was created. It is now available.  

Visit the application dashboard for more details.  

Video demonstration of set up and the application can be found [here](https://drive.google.com/file/d/18IjGhudcVxylOxLnVyCGQKt84Y5njKYH/view?usp=sharing). Please download, extract and view the video on a large screen. I apologise for the quality. The video demonstration is for an older version. Few functionalities have been added since it was recorded.  

---

Author: pawanmsr  
Last updated: March 7, 2021  
Hours clocked: 21    