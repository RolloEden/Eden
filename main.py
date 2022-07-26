from flask import Flask, redirect, url_for, render_template, request, flash
from werkzeug.utils import secure_filename
import datetime as dt
import shutil
import time
import os

main_directory = os.getcwd()

app = Flask(__name__)
app.secret_key = 'NFGPOESBHGPIUEARGBAWGRGPOUIREWA12321'
app.config['UPLOAD_PATH'] = str(main_directory) + '\\static'


banned = False


banned_ips_list = []
file = open('bannedips.txt', 'r')
content = (str(file.read())).split('\n')
file.close()
for banned_ip in content:
    banned_ips_list.append(banned_ip)




def logged(info):
    # ask for either usernma or password
    os.chdir(main_directory)
    d = {'username':0, 'password':1}
    file = open('logged.txt', 'r')
    content = file.read()
    if content != '':
        filecont = content.split('\n')
        result = filecont[int(d[info])]
        file.close()
        return result
    else:
        file.close()
        return False










@app.route('/', methods=['GET'])
def home():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    if logged('username') != False:
        # loading feed
        all_posts = []
        os.chdir(main_directory)
        os.chdir('POSTS')
        dir_ = os.getcwd()
        post_folders = os.listdir()
        for post_folder in post_folders:

            # changing directories
            os.chdir(str(post_folder))

            # creating a sublist <=> to append it to the all_posts list
            sub_list = []

            # appending user's name to the sublist - 0
            users_name = ''
            for ch in post_folder:
                if not ch.isdigit():
                    users_name += ch
            sub_list.append(users_name)

            # appending the date - 1
            os.chdir(main_directory)
            os.chdir('POSTS')
            os.chdir(str(post_folder))
            file = open('date.txt', 'r')
            new_date = file.read()
            file.close()
            sub_list.append(str(new_date))

            # appending the profile picture - 2
            os.chdir(main_directory)
            os.chdir('static')
            files = os.listdir()
            for ext in ['.jpg', '.png', '.img']:
                if (str(users_name) + str(ext)) in files:
                    prof_pic = (str(users_name) + str(ext))
                else:
                    pass
            sub_list.append(prof_pic)

            # appending the title and description of the post to the sublist - 3
            os.chdir(main_directory)
            os.chdir('POSTS')
            os.chdir(str(post_folder))
            file = open('postitself.txt', 'r')
            content = file.read()
            file.close()
            content = content.split('\n')
            for s in content:
                sub_list.append(s)

            # appending the comments from the post to the sublist
            file = open('likes.txt', 'r')
            content = file.read()
            file.close()
            content = content.split('\n')
            sub_list.append(len(content))

            all_posts.append(sub_list)
            os.chdir(dir_)


        # loop's finished
        os.chdir(main_directory)
        all_posts.reverse()

        # all_posts = [ [username, pic, date, title, content, likes],      [username, pic, date, title, content, likes] ]
        #                      ^1Patrick                                            ^2David
        return render_template('home.html', posts=all_posts, logged_as=logged('username'))
    else:
        return redirect('/signin')






        # CREATE A POST


@app.route('/create-post')
def create_post():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    if logged('username') != False:
        return render_template('create-post.html', logged_as=logged('username'))
    else:
        return redirect('/signin')

@app.route('/checknewpost', methods=['POST', 'GET'])
def checknewpost():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    if logged('username') == False:
        return redirect('/signin')
    # redirecting user that arent logged in
    if logged == False:
        return redirect('/signin')

    # changing directory

    os.chdir(main_directory)
    os.chdir('POSTS')
    all_file_names = os.listdir() 

    users_name = logged('username')

    
    
    numbers_lst = []

    for file_name in all_file_names:
        number_chrs = ''
        for ch in file_name:
            if ch.isdigit() == True:
                number_chrs += ch
        numbers_lst.append(int(number_chrs))
            

    last_highest_number = int(max(numbers_lst) + 1)


    users_file_name = str((int(last_highest_number))) + users_name


    # changing directory
    os.chdir('POSTS')
    # creating the file
    os.mkdir(users_file_name)
    # joining a new path
    os.chdir(users_file_name)
    
    
 
    # creating the files inside the folder
    # creating 'postitself.txt' & 'like.txt' files
    new_file = open('postitself.txt', 'w')
    new_file.write(str(request.form['title']) + '\n' + str(request.form['content']))
    new_file.close()
    new_file2 = open('likes.txt', 'w')
    new_file2.close()

    # creating 'date.txt' file
    date = str((str(dt.date.today())).replace('-','.'))
    date = date.split('.')
    date.reverse()
    print(date)
    new_date = ''

    for el in date: 
        new_date += el + '.'
    print(new_date)

    file = open('date.txt', 'w')
    file.write(str(new_date[:-1]))
    file.close()
    print(str(new_date[:-1]))
    return redirect('/')




        # SIGN IN


@app.route('/signin')
def signin():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    return render_template('signin.html', redirected=False)

@app.route('/checksignin', methods=['GET', 'POST'])
def checksignin():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass

    os.chdir(main_directory)
    list_of_users = ((open('list of users.txt', 'r')).read()).split('\n')
    line_nr = 0
    real_password = ''
    for line in list_of_users:
        if request.form['username'] in line:
            real_password = (line.split(' '))[-1]


    if str(request.form['password']) == str(real_password):
        # logged in successfully
        logged_file = open('logged.txt', 'w')
        os.chdir(main_directory)
        logged_file.write(str(request.form['username']) + '\n' + str(request.form['password']))
        logged_file.close()
        #return '<h2>LOGGED IN SUCCESFULLY</h2>'
        return redirect('/')
    else:
        #logged in unsuccessful
        return redirect('/signin')




        # SIGN UP


@app.route('/signup')
def signup():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    return render_template('signup.html')

@app.route('/checksignup', methods=['GET', 'POST'])
def checksignup():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    os.chdir(main_directory)
    file = open('list of users.txt', 'r')
    content = file.read()
    file.close()
    if request.form['username'] not in content and str(request.form['password']) == str(request.form['password2']):
        # adding the user on the "list of users" file
        file = open('list of users.txt', 'a')
        file.write('\n' + str(request.form['username']) + ' ' + str(request.form['password']))
        file.close()
        # creating a user's directory
        os.chdir(main_directory)
        os.chdir('Accounts')
        os.mkdir(str(request.form['username']))
        os.chdir(str(request.form['username']))
        file = open('bio.txt', 'w')
        file.write('')
        file.close()
        # create profile picture file (empty)
        os.chdir(main_directory)
        os.chdir('static')
        destination = str(os.getcwd() + '\\' + request.form['username'] + '.png')
        shutil.copyfile(os.getcwd() + '\\default.png', destination)
        file.close()
        return redirect('/')
    else:
        return redirect('/signup')



        # LOG OUT

@app.route('/logout')
def logout():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    if logged('username') == False:
        return redirect('/signin')
    file = open('logged.txt', 'w')
    file.write('')
    file.close()
    return redirect('/signin')





        # ACCOUNTS

@app.route('/<account>')
def Account(account):
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    # getting the bio
    os.chdir(main_directory)
    os.chdir('Accounts')
    os.chdir(account)
    file = open('bio.txt', 'r')
    account_bio = file.read()
    file.close()
    # getting the profile picture
    os.chdir(main_directory)
    os.chdir('static')
    all_files = os.listdir()
    the_profile_picture = ''
    for ext in ['.jpg', '.png', '.img']:
        if (str(account) + str(ext)) in all_files:
            the_profile_picture = (str(account) + str(ext))
        else:
            pass
    # getting the posts posted by the user whos account is
    os.chdir(main_directory)
    os.chdir('POSTS')
    all_file_names = os.listdir()
    all_posts = []
# START
    dir_ = os.getcwd()
    for post_folder in all_file_names:
        os.chdir(main_directory)
        os.chdir('POSTS')
        # changing directories
        os.chdir(str(post_folder))

        # creating a sublist <=> to append it to the all_posts list
        sub_list = []

        # appending user's name to the sublist
        users_name = ''
        for ch in post_folder:
            if not ch.isdigit():
                users_name += ch

        if users_name == account:
            sub_list.append(users_name)

            # appending the date
            os.chdir(main_directory)
            os.chdir('POSTS')
            os.chdir(str(post_folder))
            file = open('date.txt', 'r')
            new_date = file.read()
            file.close()
            sub_list.append(str(new_date))

            # appending the title and description of the post to the sublist
            os.chdir(main_directory)
            os.chdir('POSTS')
            os.chdir(str(post_folder))
            file = open('postitself.txt', 'r')
            content = file.read()
            file.close()
            content = content.split('\n')
            for s in content:
                sub_list.append(s)

            # appending the comments from the post to the sublist
            file = open('likes.txt', 'r')
            content = file.read()
            file.close()
            content = content.split('\n')
            sub_list.append(len(content))

            all_posts.append(sub_list)
            os.chdir(dir_)
        else:
            pass

    os.chdir(main_directory)
    all_posts.reverse()
# FINISH
    if str(logged('username')) == str(account):
        return render_template('account.html', acc=account, bio=account_bio, logged_as=logged('username'), profile_picture=the_profile_picture, posts=all_posts, personal=True)
    else:
        return render_template('account.html', acc=account, bio=account_bio, logged_as=logged('username'), profile_picture=the_profile_picture, posts=all_posts,  personal=False)








        # EDIT ACCOUNT
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    if logged('username') == False:
        return redirect('/signin')
    return render_template('edit-account.html', logged_as=logged('username'))

        # CONIFRM EDIT
@app.route('/comfirm_edit_bio', methods=['GET', 'POST'])
def confirm_edit_bio():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    usrname = str(logged('username'))
    os.chdir(main_directory)
    os.chdir('Accounts')
    os.chdir(usrname.capitalize())
    
    file = open('bio.txt', 'w')
    file.write(request.form['new_bio'])
    file.close()
    return redirect(str('/' + str(logged('username'))))


        # EDIT PROFILE IMAGE
@app.route('/editimage', methods=['POST', 'GET'])
def editimage():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    if request.method == 'POST':
        f = request.files['file_name']
        os.chdir(main_directory)
        os.chdir('static')
        print(os.listdir())
        the_file = ''
        for file in os.listdir():
            if logged('username') in file:
                the_file = file
        os.chdir(main_directory)
        os.chdir('static')
        os.remove(the_file)
        f.save(the_file)
        return redirect('/' + str(logged('username')))
    return render_template('edit-image.html', logged_as=logged('username'))


        # CHANGE PASSWORD
@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    os.chdir(main_directory)
    file = open('list of users.txt', 'r')
    content = file.read()
    file.close()
    if str(request.form['old_password']) in content and str(request.form['new_password']) == str(request.form['new_password2']):
        done = False
        users_new_line = ''
        after_ = ''
        before_ = ''
        for line in content.split('\n'):
            if str(logged('username')) in line:
                users_new_line = (line.split(' '))[0] + ' ' + str(request.form['new_password'])
                done = True
            elif done:
                after_ += line + '\n'
            elif str(logged('username')) in line:
                before_ += line + '\n'
        file = open('list of users.txt', 'w')
        file.write((before_ + '\n' + users_new_line + '\n' + after_).strip)
        file.close()
        return redirect('/' + str(logged('username')))
    else:
        return redirect('/edit')



        # USERS
@app.route('/users')
def users():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    if logged('username') == False:
        return redirect('/signin')
    # all users list
    all_users = []
    file = open('list of users.txt', 'r')
    content = file.read()
    file.close()
    for user in content.split('\n'):
        all_users.append(user)
    return render_template('users.html', users=all_users, logged_as=logged('username'))




        # CONTACT
@app.route('/contact')
def contact():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    else:
        pass
    return render_template('contact.html', logged_as=logged('username'))



        # RULES
@app.route('/rules')
def rules():
    return render_template('rules.html', logged_as=logged('username'))

        # ABOUT US
@app.route('/aboutus')
def aboutus():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    if logged('username') == False:
        return redirect('/signin')
    return render_template('aboutus.html', logged_as=logged('username'))


        # FORGOT PASSWORD
@app.route('/forgot-password')
def forgot_password():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        file = open('logged.txt', 'w')
        file.write('')
        file.close()
        return redirect('/')
    return render_template('forgot_password.html')



if __name__ == '__main__':
    app.run()(debug=False,host="0.0.0.0")
