import app.ebayclass as ebay
import app.sqlmodel as sql
import app.telegramclass as telegram
import sys


def alert():
    links = [rows["link"] for rows in sql.getLinks()]
    if links:
        for link in links:
            addPost(link, True)
    print("Success")

def links(show, remove, clear, add, init):
    if show:
        links = [(rows["id"], rows["link"])for rows in sql.getLinks()]
        print("id     link")
        if links:
            for id, link in links:
                print("{0:<{1}}{2}".format(id, 8 - len(str(id)) ,link))
    elif remove:
        sql.removeLink(remove)
        print("Link removed")
    elif clear:
        sql.clearPostDatabase()
        print("Post database cleared")
    elif add:
        sql.addLink(add)
        addPost(add)
        print("Link and post added to the database")
    elif init:
        links = [rows["link"] for rows in sql.getLinks()]
        if links:
            for link in links:
                addPost(link)
        print("database initialised")


def addPost(link, toSend=False):
    posts = ebay.getPost(link)
    for post in posts:
        if not sql.postExist(post.id):
            sql.addPost([post])
            if toSend:
                telegram.sendMessage("{}\n\n{} ({})\n\n{}".format(post.title, post.price, post.city, post.link))


if __name__ == "__main__":
    alert()