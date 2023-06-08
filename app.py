from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

client = MongoClient('mongodb+srv://wjsckdals108:ckdals108@cluster0.oxx6bv6.mongodb.net/?retryWrites=true&w=majority')

db = client.TeamProject

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/members", methods=["GET"])
def member_get():
    all_members = list(db.project_2_members.find({},{'_id':False}))
    return jsonify({'result':all_members})

@app.route("/update", methods=["POST"]) #/rely로 받음
def modify_post():
   name_receive = request.form['name_give']
   desc1_receive = request.form['desc1_give']
   desc2_receive = request.form['desc2_give']
   desc3_receive = request.form['desc3_give']
     
   myquery = {"name":name_receive}
   newvalue1 = {"$set":{"description1":desc1_receive}}
   newvalue2 = {"$set":{"description2":desc2_receive}}
   newvalue3 = {"$set":{"description3":desc3_receive}}

   db.project_2_members.update_one(myquery,newvalue1)
   db.project_2_members.update_one(myquery,newvalue2)
   db.project_2_members.update_one(myquery,newvalue3)

   return jsonify({'msg':'수정완료!'})

#댓글 조회
'''
/getcomments로 요청 시 GET방식으로 전달된 name을 받아서 name에 해당하는 인원의 Comments 테이블에
있는 데이터를 모두 받아와 'result'로 넘겨준다.
'''
@app.route('/getcomments',methods=['GET'])
def getComments():
    name_receive = str(request.args.get('name'))
    ct = list(db.project_2_comments.find({'name':name_receive},{'_id':False}))
    
    return jsonify({'result':ct})

#댓글 등록 
'''
/addcomments로 요청 시 POST방식으로 넘어온 데이터를 각 변수에 저장 후, DB에 name, cid, text 속성 값으로 
DB에 저장한다.
'''
@app.route('/addcomments',methods=['POST'])
def addComments():
    name_receive = request.form['name_give']
    cid_receive = request.form['cid_give']
    text_receive = request.form['text_give']
    
    doc = {
        'name' : name_receive,
        'cid' : cid_receive,
        'text' : text_receive
    }
    
    db.project_2_comments.insert_one(doc)
    
    return jsonify({'result':'댓글 등록 성공'})

#댓글 수정
'''
/updatecomments로 요청 시 PUT방식을 사용하고, 어떤 댓글인지를 식별하기 위해 name과 cid 그리고 변경할 댓글 문장을 text
로 받습니다. comments 테이블에서 name과 cid에 해당하는 데이터를 찾고 text를 변경하여 적용합니다.
'''
@app.route('/updatecomments',methods=['PUT'])
def updateComments():
    #name_receive = request.args.get('name')
    #cid_receive = request.args.get('cid')
    name_receive = request.form['name_give']
    cid_receive = request.form['cid_give']
    text_receive = request.form['text_give']
    db.project_2_comments.update_one(
        {'name':name_receive, 'cid':cid_receive},
        {"$set": {
            'text': text_receive
        }}
    )
    
    return jsonify({'result':'댓글 수정 성공'})

#댓글 삭제
'''
/deletecomments로 요청 시 삭제할 댓글을 식별하기 위해 name과 cid를 받고 comments 테이블에서 name과 cid가 동일한
데이터 값을 삭제합니다.
'''
@app.route('/deletecomments',methods=['DELETE'])
def deleteComments():
    name_receive = request.args.get('name')
    cid_receive = request.args.get('cid')
    
    db.project_2_comments.delete_one(
        {'name':name_receive, 'cid':cid_receive}
    )
    
    return jsonify({'result':'댓글 삭제 성공'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)