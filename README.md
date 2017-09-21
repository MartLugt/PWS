# PWS
In this repository, you put all the code you write, as long as it works and is tested. 
If the code isn't tested, commit it, but don't push. 

###### !! IMPORTANT !!

When making changes to code which other code is dependant on, make sure to do this on another branch 
(see how to below). This makes it so that the other code doesn't break while you are making changes, and the other person 
can keep coding. This also means that you can take multiple days / weeks editing the code 
without stopping the other person from doing his work. 

For example:

If file3 uses functions from file2, and file2 is suddenly deleted or edited, file3 will no longer work. If the other person 
is working on file3 or another file that uses functions from file3, he won't be able to test / run the code.

###### //!! IMPORTANT !!

Quick overview of how it works:
 * Pull (VCS / Git / Pull) to get the work of the other person on your computer
 * Then edit/code/write whatever
 * Commit (Ctrl - K) to let Git know you made changes and save them. If you don't commit the changes, you can't push them.
 * Push (Ctrl - Shift - K) so the other person can see your changes. If you don't push, the files won't be accessible thru the cloud.

##### Commit message
 
Make sure to actually type a meaningful commit message, this will make it easier to troubleshoot and will be more helpfull for the other person.

For Example:

Good:

"Added file1, file2 and file3.
Changed file918 so that it now can accept more data. Fixed bug #67 in file45"

Bad:

"Changed some shit"

##### Why use Git?

Using Git we can easily see who exactly wrote what, we can see exactly when what was written and we can easily backup 
the code. When there is a bug, we can compare the code to the previous working version and easily see what the problem is.

##### Bla bla bla

Use lots of boring comments so the other nigga can understand the mess I just coded.

Easily make a TODO list by writing "#TODO: blablabla". PyCharm will pick this up and include it in the commit message.
It will also make it easily accessible in the TODO menu (Alt - 6).

Noice

##### Bugs

When you find a bug during testing, try to fix it. If you can't fix it / don't have time, report it on GitHub under 'Issues'.
Give it a title, add a**meaningful**description so that the person fixing the bug actually knows what the bug is**and how to reproduce it**, 
and assign someone. Yourself if you will fix the bug yourself or the other person if the bug is in his part of the code / you can't fix it.
Also label it BUG.

##### Not very important questions

Do the same thing as with bugs, but label it question / help wanted.

##### How to push to another branch

First, find where it says Git: master in the bottom right corner. Click it, select the branch you want and click Checkout.
You are now editing that branch. The files in this branch might be different than master, so make sure to select the right branch before starting.

Now just do what you would normally do, but make sure you are in the right branch when committing. 
 
When the branch is done and tested, merge it with master.


Software
-
[Pycharm](https://www.jetbrains.com/pycharm/) (or any other Python IDE, this one is easy to use and great)

[Git](https://git-scm.com/downloads)  (needed for github)

[TortoiseGit](https://tortoisegit.org/) (optional, makes it easy to commit and do other git stuff from file explorer)