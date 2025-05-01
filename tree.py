import graphviz
import os
import itertools

# كلاس لتمثيل عقدة في الشجرة
class Node:
    def __init__(self, unique_id, action: int, info: dict = None):
        if not isinstance(unique_id, int):
            raise TypeError("Unique ID must be an integer.")
        # The action here represents the action TAKEN from the parent state to reach this state.
        # For the root node, action doesn't have a parent action, so we can use a placeholder like -1.
        if not isinstance(action, int):
            raise TypeError("Action must be an integer.")

        self._id = unique_id
        self.action = action
        self.info = info if info is not None else {}
        if not isinstance(self.info, dict):
            raise TypeError("Info must be a dictionary.")

        self.children = []

    def add_child(self, child_node):
        """يضيف عقدة كابن للعقدة الحالية"""
        if isinstance(child_node, Node):
            self.children.append(child_node)
        else:
            print(f"Error: Can only add Node objects as children to node with ID {self._id}.")

    def __repr__(self):
        """تمثيل العقدة (للطباعة)"""
        return f"Node(id={self._id}, action={self.action}, info={self.info})"


# كلاس لإدارة الشجرة وتوليد التمثيل المرئي
class VisualTree:
    def __init__(self, root_action: int = -1, root_info: dict = None):
        """يهيئ الشجرة بعقدة جذرية"""
        self._node_id_counter = itertools.count()
        root_id = next(self._node_id_counter)
        self.root = Node(root_id, root_action, root_info)

        # سنعيد بناء الرسم في render_and_display
        self._dot = None

    def _get_next_id(self):
        """يولد ويعيد المعرف الفريد التالي"""
        return next(self._node_id_counter)

    # تم تعديلها لترجع العقدة نفسها والأب
    def _find_node_recursive(self, target_id, current_node: Node, parent_node: Node):
        """دالة مساعدة (خاصة) للبحث عن عقدة بمعرف فريد وأبوها بشكل تكراري"""
        if current_node is None:
            return None, None

        if current_node._id == target_id:
            return current_node, parent_node

        for child in current_node.children:
            found_node, found_parent = self._find_node_recursive(target_id, child, current_node)
            if found_node:
                return found_node, found_parent

        return None, None

    def find_node_by_id(self, target_id) -> Node | None:
        """تبحث وتُرجع العقدة التي لها المعرف الفريد المحدد."""
        found_node, _ = self._find_node_recursive(target_id, self.root, None)
        return found_node

    def _build_graphviz(self, node: Node):
        """دالة مساعدة (خاصة) لبناء رسم Graphviz بشكل تكراري من الشجرة"""
        if node is None or self._dot is None:
            return

        node_id_str = str(node._id)

        node_label_lines = [f"ID: {node._id}"]
        # لا نعرض الـ action -1 للجذر لأنه ليس حركة اتخذت
        if node != self.root or node.action != -1:
            node_label_lines.append(f"Action: {node.action}")


        if node.info:
            for key, value in node.info.items():
                # تحويل القيمة إلى string مع بعض التنسيق للقيم العائمة الطويلة
                display_value = f"{value:.2f}" if isinstance(value, float) else str(value)
                node_label_lines.append(f"{key}: {display_value}")

        node_label = "\n".join(node_label_lines)

        self._dot.node(node_id_str, label=node_label)

        for child in node.children:
            child_id_str = str(child._id)
            self._dot.edge(node_id_str, child_id_str)
            self._build_graphviz(child)

    # تم تعديلها لترجع كائن العقدة المضاف
    def add_node(self, parent_id, child_action: int, child_info: dict = None) -> Node | None:
        """
        يضيف عقدة جديدة كابن للعقدة التي بمعرفها الفريد parent_id.
        يرجع كائن العقدة الابن الجديدة المضافة، أو None إذا فشلت الإضافة.
        """
        parent_node = self.find_node_by_id(parent_id) # استخدام الدالة الجديدة للعثور على الأب

        if parent_node:
            new_node_id = self._get_next_id()
            new_node = Node(new_node_id, child_action, child_info)
            parent_node.add_child(new_node)
            # print(f"Added node (ID: {new_node_id}, Action: {child_action}) as child of node with ID: {parent_id}") # إزالة الطباعة المزعجة أثناء بناء الشجرة الكبيرة
            return new_node # إرجاع كائن العقدة الجديدة
        else:
            # print(f"Error: Parent node with ID {parent_id} not found. Cannot add node with action {child_action}.") # إزالة الطباعة المزعجة
            return None

    def remove_node(self, node_id_to_remove):
        """
        يزيل عقدة بالبحث عن معرفها الفريد وجميع أبنائها.
        """
        if self.root._id == node_id_to_remove:
            print(f"Error: Cannot remove root node (ID: {node_id_to_remove}) directly in this example.")
            return

        # البحث عن العقدة التي سيتم إزالتها وأبوها
        node_to_remove, parent_of_node = self._find_node_recursive(node_id_to_remove, self.root, None)

        if node_to_remove is None:
            print(f"Error: Node with ID {node_id_to_remove} not found.")
            return

        # إزالة العقدة من قائمة أبناء الأب
        if parent_of_node: # التأكد أن هناك أب قبل محاولة الإزالة منه (الجذر ليس له أب هنا)
            try:
                parent_of_node.children.remove(node_to_remove)
                print(f"Removed node with ID: {node_id_to_remove} (Action: {node_to_remove.action}, and its subtree).")
            except ValueError:
                print(f"Internal Error: Node ID {node_id_to_remove} found but node object not in parent's children list.")
            except Exception as e:
                print(f"An unexpected error occurred during removal: {e}")


    def render_and_display(self):
        """يعيد بناء رسم Graphviz للحالة الحالية للشجرة ويعرضه"""
        print("\nRendering and displaying tree...")
        # مسح الرسم الحالي لإعادة بنائه
        self._dot = graphviz.Digraph(comment='Minimax Tree', node_attr={'shape': 'box', 'style': 'rounded'})
        self._dot.attr(rankdir='TB') # اتجاه الرسم: من الأعلى للأسفل (Top-Bottom)

        # إعادة بناء الرسم من بنية الشجرة الحالية
        self._build_graphviz(self.root)

        # حفظ الرسم وعرضه
        try:
            # filename='minimax_tree'
            self._dot.render('minimax_tree', view=True, cleanup=True, format='png')
            print("Visualization updated and displayed.")
        except graphviz.backend.execute.ExecutableNotFound:
            print("\nError: Graphviz executable not found!")
            print("Please make sure Graphviz is installed and its directory is in your system's PATH.")
            print("Download from: https://graphviz.org/download/")
        except Exception as e:
            print(f"An error occurred during rendering: {e}")

    # تم إزالة find_nodes_by_action لأنها غير ضرورية للدمج الحالي

# --- مثال على الاستخدام ---

if __name__ == "__main__":
    # إنشاء شجرة بعقدة جذرية (action=1, info={'name': 'Start'})
    # المعرف الفريد الأول سيكون 0
    tree = VisualTree(1, {'name': 'Start'})
    print(f"Initial tree created with root (Action: 1, ID: {tree.root._id}).")
    root_id = tree.root._id # نحتفظ بمعرف الجذر

    # عرض الشجرة الابتدائية (ستكون فقط العقدة الجذرية بمعرف 0)
    tree.render_and_display()

    input("\nPress Enter to add initial nodes (Actions 2, 3, 4, 5, 6 under different parents using parent IDs)...")
    # إضافة بعض العقد بمعلومات مختلفة في القاموس info، باستخدام ID الأب
    # سنحتفظ بـ IDs للعقد التي قد نريد حذفها لاحقاً
    child1_id = tree.add_node(root_id, 2, {'name': 'Action A', 'cost': 10}) # الابن الأول للجذر (action=2) - ID 1
    child2_id = tree.add_node(root_id, 3, {'name': 'Action B', 'description': 'Processing step'}) # الابن الثاني للجذر (action=3) - ID 2

    # نتأكد أن الإضافة تمت بنجاح قبل محاولة استخدام الـ IDs
    if child1_id is not None:
        grandchild1_of_2_id = tree.add_node(child1_id, 4, {'name': 'Sub-Action A1', 'status': 'completed'}) # ابن العقدة ذات ID child1_id (action=4) - ID 3
        grandchild2_of_2_id = tree.add_node(child1_id, 5, {'name': 'Sub-Action A2', 'data_id': 'xyz123', 'flag': True}) # ابن العقدة ذات ID child1_id (action=5) - ID 4
    else:
        grandchild1_of_2_id, grandchild2_of_2_id = None, None

    if child2_id is not None:
        grandchild1_of_3_id = tree.add_node(child2_id, 6, {'name': 'Sub-Action B1', 'progress': 0.5}) # ابن العقدة ذات ID child2_id (action=6) - ID 5
    else:
        grandchild1_of_3_id = None

    # إضافة عقدتين لهما نفس الـ action (مثلاً action 4) ولكن آباء مختلفين
    if child2_id is not None:
         # نضيف تحت العقدة ذات ID child2_id (action 3)
        duplicate_action_node1_id = tree.add_node(child2_id, 4, {'name': 'Sub-Action B2 - Duplicate Action 4'}) # ID 6
    else:
        duplicate_action_node1_id = None

    if grandchild1_of_2_id is not None:
        # نضيف تحت العقدة ذات ID grandchild1_of_2_id (action 4)
        duplicate_action_node2_id = tree.add_node(grandchild1_of_2_id, 4, {'name': 'Sub-Action A1.1 - Duplicate Action 4'}) # ID 7
    else:
        duplicate_action_node2_id = None


    # عرض الشجرة بعد الإضافات
    tree.render_and_display()

    print("\nIDs of some added nodes:")
    print(f"Root ID: {root_id}")
    print(f"Child 1 ID (Action 2): {child1_id}")
    print(f"Child 2 ID (Action 3): {child2_id}")
    print(f"Grandchild 1 of ID {child1_id} (Action 4): {grandchild1_of_2_id}")
    print(f"Grandchild 2 of ID {child1_id} (Action 5): {grandchild2_of_2_id}")
    print(f"Grandchild 1 of ID {child2_id} (Action 6): {grandchild1_of_3_id}")
    print(f"Duplicate Action 4 under ID {child2_id}: {duplicate_action_node1_id}")
    print(f"Duplicate Action 4 under ID {grandchild1_of_2_id}: {duplicate_action_node2_id}")


    # # مثال على البحث عن عقدة بالـ action (لإظهار كيفية العثور على ID إذا لم تكن تعرفه مباشرة)
    # print("\nSearching for nodes with Action 4:")
    # action_4_nodes = tree.find_nodes_by_action(4)
    # if action_4_nodes:
    #     print(f"Found {len(action_4_nodes)} node(s) with Action 4:")
    #     for node in action_4_nodes:
    #         print(f" - Node ID: {node._id}, Parent ID (if not root): {next((p._id for p in [tree.root] + [c for parent in tree.root.children for c in parent.children if node in parent.children] for c in parent.children if node in parent.children), None)}, Info: {node.info}") # عرض الأب معقد قليلا هنا
    #         # طريقة أسهل لعرض الأب:
    #         _, parent = tree._find_node_by_id_and_parent(node._id, tree.root, None)
    #         parent_id_display = parent._id if parent else "None (Root)"
    #         print(f"   - Node ID: {node._id}, Parent ID: {parent_id_display}, Info: {node.info}")

    # else:
    #     print("No nodes found with Action 4.")


    if child1_id is not None:
        input(f"\nPress Enter to remove node with ID {child1_id} (Action 2, and its subtree)...")
        # إزالة العقدة التي الـ ID الخاص بها هو child1_id (وهي العقدة التي action الخاص بها 2 تحت الجذر)
        # هذا سيؤدي أيضاً لإزالة أبنائها وأبناء أبنائها
        tree.remove_node(child1_id)
        # عرض الشجرة بعد الحذف
        tree.render_and_display()
    else:
        print("\nSkipping removal of node with ID (was not added successfully).")


    input("\nPress Enter to try removing a non-existent node (ID 999)...")
    tree.remove_node(999) # محاولة إزالة عقدة غير موجودة بالـ ID
    tree.render_and_display() # عرض للتأكد أنه لم يحدث تغيير


    if duplicate_action_node1_id is not None:
        input(f"\nPress Enter to remove node with ID {duplicate_action_node1_id} (Action 4, under Action 3)...")
        # إزالة إحدى العقدتين اللتين لهما نفس الـ action 4، بالاعتماد على الـ ID الفريد الخاص بها
        tree.remove_node(duplicate_action_node1_id)
         # عرض الشجرة بعد الحذف
        tree.render_and_display()
    else:
         print("\nSkipping removal of duplicate action node 1 (was not added successfully).")


    if child2_id is not None:
        input(f"\nPress Enter to add another node (Action 7) under node with ID {child2_id} (Action 3)...")
        # نضيف تحت العقدة ذات ID child2_id (action 3)
        tree.add_node(child2_id, 7, {'name': 'Sub-Action B3', 'details': 'more info'})
        # عرض الشجرة بعد الإضافة الجديدة
        tree.render_and_display()
    else:
        print("\nSkipping adding node under child 2 (was not added successfully).")


    input("\nPress Enter to try adding to a non-existent parent (ID 9999)...")
    tree.add_node(9999, 200, {'error': 'Should Fail'}) # محاولة الإضافة لأب غير موجود بالـ ID
    tree.render_and_display() # عرض للتأكد أنه لم يحدث تغيير

    input("\nPress Enter to exit.")
