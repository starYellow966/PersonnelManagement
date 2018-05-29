# class TreeNode:
#     '''基本的树状结构中节点的数据结构
    
#     用于bootstrap treeview节点的数据结构
    
#     Variables:
#         id {str} -- 节点id
#         text {str} -- 节点内容
#         parent_id {str} -- 节点父节点id
#         nodes {list<dict>} -- 子节点
#         icon {str} -- 节点的icon
#     '''

#     def __init__(self, tid, text, parent_id):
#         self.id = tid
#         self.text = text
#         self.parent_id = parent_id
#         self.nodes = None
#         self.icon = "glyphicon glyphicon-bed"

#     def __repr__(self):
#         return u'id:{},text:{}, nodes:{}' .format(self.id, self.text, self.nodes)

#     def add_nodes(self, nodes):
#         '''添加子节点
        
#         Arguments:
#             nodes {list<TreeNode>} -- 子节点list
#         '''
#         if(nodes is not None):
#             nodes = convert_to_dict(nodes)
#             if(self.nodes is None):
#                 self.nodes = nodes
#             else:
#                 self.nodes = self.nodes + nodes

#     def convert_to_dict(self, nodes):
#         results = None
#         if(nodes is not None):
#             results = []
#             for x in nodes:
#                 results.append(x.__dict__)

#         return results
