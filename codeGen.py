import pickle
dtree_dict=pickle.load(open("dtree_dm.pklz","rb"))
dtree=dtree_dict['dtree_dm']
def recurse(left, right, tree, value, threshold, features, node, s1,scode):
    if (threshold[node] != -2):
        scode+=\
            "if ( " + features[node] + " <= " + str(threshold[node]) + " ) {"
        if left[node] != -1:
            s1,scode=recurse (left, right, tree, value,threshold, features,left[node],s1,scode)
            scode+= "} else {\n"
            if right[node] != -1:
                s1,scode=recurse (left, right, tree, value,threshold, features,right[node],s1,scode)
                scode+= "}\n"
    else:
        #print((node[0][0]))
        #print(node[0][0])
        scode+="*value="+str(value[node][0][0])+";\n"
        s1+=tree.tree_.n_node_samples[node]/(tree.tree_.n_node_samples[0]+0.0)
    return s1,scode

def genCode(modName,tree, feature_names):
    left      = tree.tree_.children_left
    right     = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features  = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value
    s1=0
    scode= 'void %s('%modName
    for f in feature_names:
        scode+= 'float '+f+','
    scode+='float *value){\n'
    
    s1,scode=recurse(left, right, tree, value,threshold, features, 0, s1,scode)
    return scode+"}\n"
   
dtree_dict=pickle.load(open("dEnsForest_dm.pklz","rb"))
dtree=dtree_dict['dtree_dm']
f=open("ensForestReg.c","w")
for i in range(5):
    code=genCode("treereg_dm_%i_"%i,dtree.estimators_[i], ["*zku","*zka"])
    f.write(code)

f.close()