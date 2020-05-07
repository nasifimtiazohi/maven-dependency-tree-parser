from sqlConnection import execute
from depTreeNode import depTreeNode

def getModuleId(module):
    #TODO refactor to be more elegant?
    #check if module exists in db
    results=execute('select * from modules where name ="{}";'.format(module))
    if not len(results)==1:
        #add the module 
        execute('insert into modules values (null, "{}");'.format(module))
        results=execute('select * from modules where name ="{}";'.format(module))
    
    return results[0]['id']

def parseCanonicalForm(s):
    s=s.split(":")
    if len(s)  < 4:
        print("error: ",s)
        return
    group, artifact, packaging, version, scope = s[0], s[1], s[2], s[3], None

    if len(s) == 5:
        scope = s[4]
    
    return group, artifact, packaging, version, scope
    
#read file
file=open('dep.txt','r')
Tree=[]
for line in file:
    Tree.append(line.replace('\n',''))



moduleId=None
root=None
group, artifact, packaging, version, scope = parseCanonicalForm(Tree[0])
moduleId= getModuleId(artifact)
root = depTreeNode(group, artifact, packaging, version, depth=0)
root.children=Tree[1:]

curLevel=[root]
depth=0




#implement BFS
while curLevel:
    depth+=1 #processing next level
    nextLevel=[] #put nodes of direct children here
    for node in curLevel:
        directChildren=[]
        indexes=[] #get the indexes of direct child in node.children
        for i in range(0,len(node.children)):
            node.children[i]=node.children[i][2:].strip()
            line=node.children[i]
            if not (line[0]=='\\' or line[0]=='+' or line[0]=='|' or line[0]=='-'):
                indexes.append(i)

        for i in range(0,len(indexes)):
            group, artifact, packaging, version, scope = parseCanonicalForm(node.children[indexes[i]])
            child = depTreeNode(group, artifact, packaging, version, scope, depth, node)
            if i != len(indexes) - 1:
                #if not last node
                child.children=node.children[indexes[i]+1:indexes[i+1]]
            else:
                child.children=node.children[indexes[i]+1:]
            directChildren.append(child)

        node.children=directChildren
        nextLevel.extend(node.children)
    curLevel=nextLevel


t=root.children[0]
#traverse DFS
def recursion(root):
    if root is None:
        return 
    print(root.artifact, root.depth)
    for child in root.children:
        recursion(child)

recursion(root)



        


