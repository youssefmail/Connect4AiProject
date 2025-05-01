import graphviz
import os
import itertools # لاستخدام عداد بسيط لتوليد IDs فريدة

# كلاس لتمثيل عقدة في الشجرة
class Node:
    # تمت إزالة الـ __eq__ والـ __hash__ التي كانت تعتمد على action
    # لأنه لم يعد فريداً عالمياً، ولن نعتمد عليهما للمساواة أو الهاش

    def __init__(self, unique_id, action: int, info: dict = None):
        """يهيئ العقدة بمعرف فريد عالمي، حقل action وقاموس info اختياري"""
        if not isinstance(unique_id, int):
             raise TypeError("Unique ID must be an integer.")
        if not isinstance(action, int):
             raise TypeError("Action must be an integer.")

        self._id = unique_id # المعرف الفريد لهذه العقدة
        self.action = action
        self.info = info if info is not None else {}
        if not isinstance(self.info, dict):
             raise TypeError("Info must be a dictionary.")

        self.children = [] # قائمة بالعقد الأبناء

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
    def __init__(self, root_action: int, root_info: dict = None):
        """يهيئ الشجرة بعقدة جذرية"""
        self._node_id_counter = itertools.count() # عداد لتوليد معرفات فريدة
        root_id = next(self._node_id_counter)
        self.root = Node(root_id, root_action, root_info)

        self._dot = graphviz.Digraph(comment='My Tree', node_attr={'shape': 'box', 'style': 'rounded'})
        self._dot.attr(rankdir='TB') # اتجاه الرسم: من الأعلى للأسفل (Top-Bottom)


    def _get_next_id(self):
        """يولد ويعيد المعرف الفريد التالي"""
        return next(self._node_id_counter)


    def _find_node_by_id_and_parent(self, target_id, current_node: Node, parent_node: Node):
        """دالة مساعدة (خاصة) للبحث عن عقدة بمعرف فريد وأبوها"""
        if current_node is None:
            return None, None

        if current_node._id == target_id:
            return current_node, parent_node

        for child in current_node.children:
            found_node, found_parent = self._find_node_by_id_and_parent(target_id, child, current_node)
            if found_node:
                return found_node, found_parent

        return None, None # لم يتم العثور على العقدة

    def _find_node_by_action(self, target_action: int, current_node: Node):
        """دالة مساعدة (خاصة) للبحث عن أول عقدة بقيمة action معينة (بحث عمق أول)"""
        # ملاحظة: هذه الدالة قد تجد أكثر من عقدة إذا تكرر الـ action
        # نرجع أول عقدة نجدها فقط
        if current_node is None:
            return None

        if current_node.action == target_action:
            return current_node

        for child in current_node.children:
            found_node = self._find_node_by_action(target_action, child)
            if found_node:
                return found_node

        return None


    def _build_graphviz(self, node: Node):
        """دالة مساعدة (خاصة) لبناء رسم Graphviz بشكل تكراري من الشجرة"""
        if node is None:
            return

        # استخدام المعرف الفريد _id كمعرف للعقدة في Graphviz (يجب أن يكون فريداً)
        node_id_str = str(node._id)

        # بناء النص الذي سيظهر داخل العقدة (يشمل Action والمعرف الفريد وبيانات Info)
        node_label_lines = [f"ID: {node._id}", f"Action: {node.action}"]

        if node.info: # إذا كان قاموس info غير فارغ
            for key, value in node.info.items():
                node_label_lines.append(f"{key}: {value}")

        node_label = "\n".join(node_label_lines)

        # إضافة العقدة للرسم
        self._dot.node(node_id_str, label=node_label)

        # إضافة الحواف للأبناء (نستخدم المعرفات الفريدة للحواف أيضاً)
        for child in node.children:
            child_id_str = str(child._id)
            self._dot.edge(node_id_str, child_id_str) # حافة من الأب (بمعرفه) إلى الابن (بمعرفه)
            self._build_graphviz(child) # تابع البناء مع الابن


    def add_node(self, parent_action: int, child_action: int, child_info: dict = None) -> int | None:
        """
        يضيف عقدة جديدة كابن لأول عقدة يتم العثور عليها بقيمة parent_action.
        يرجع المعرف الفريد للعقدة الابن الجديدة المضافة، أو None إذا فشلت الإضافة.
        """
        # البحث عن العقدة الأب باستخدام الـ action
        parent_node = self._find_node_by_action(parent_action, self.root)

        if parent_node:
            # توليد معرف فريد للعقدة الجديدة
            new_node_id = self._get_next_id()
            new_node = Node(new_node_id, child_action, child_info)
            parent_node.add_child(new_node)
            print(f"Added node (ID: {new_node_id}, Action: {child_action}) as child of node with Action: {parent_action} (ID: {parent_node._id})")
            # لا نستدعي التحديث هنا تلقائيًا
            return new_node_id # إرجاع المعرف الفريد للعقدة الجديدة
        else:
            print(f"Error: Parent node with action {parent_action} not found. Cannot add node with action {child_action}.")
            return None # فشل الإضافة


    def remove_node(self, node_id_to_remove):
        """
        يزيل عقدة بالبحث عن معرفها الفريد وجميع أبنائها.
        """
        if self.root._id == node_id_to_remove:
             print(f"Error: Cannot remove root node (ID: {node_id_to_remove}) directly in this example.")
             return

        # البحث عن العقدة التي سيتم إزالتها وأبوها باستخدام المعرف الفريد
        node_to_remove, parent_of_node = self._find_node_by_id_and_parent(node_id_to_remove, self.root, None)

        if node_to_remove is None:
            print(f"Error: Node with ID {node_id_to_remove} not found.")
            return

        # إزالة العقدة من قائمة أبناء الأب
        try:
             # البحث عن العقدة في قائمة أبناء الأب باستخدام المعرف الفريد أو الكائن نفسه
             # بما أننا حصلنا على كائن العقدة الأصلية، يمكن استخدام .remove() مباشرة
             parent_of_node.children.remove(node_to_remove)
             print(f"Removed node with ID: {node_id_to_remove} (Action: {node_to_remove.action}, and its subtree).")
             # لا نستدعي التحديث هنا تلقائيًا
        except ValueError:
             # Should not happen if _find_node_by_id_and_parent is correct, but as a safeguard
             print(f"Internal Error: Node ID {node_id_to_remove} found but node object not in parent's children list.")
        except Exception as e:
            print(f"An unexpected error occurred during removal: {e}")


    def render_and_display(self):
        """يعيد بناء رسم Graphviz للحالة الحالية للشجرة ويعرضه"""
        print("\nRendering and displaying tree...")
        # مسح الرسم الحالي لإعادة بنائه
        self._dot = graphviz.Digraph(comment='My Tree', node_attr={'shape': 'box', 'style': 'rounded'})
        self._dot.attr(rankdir='TB') # اتجاه الرسم: من الأعلى للأسفل (Top-Bottom)

        # إعادة بناء الرسم من بنية الشجرة الحالية
        self._build_graphviz(self.root)

        # حفظ الرسم وعرضه
        try:
            # حفظ كملف DOT وعرضه
            # يمكنك تغيير format='png' أو 'jpg' أو 'svg' حسب الرغبة
            # filename='current_tree' يعني أن الملف سيكون اسمه current_tree.gv وسيتم حفظ الصورة باسم current_tree.gv.png (أو حسب الفورمات)
            self._dot.render('current_tree', view=True, cleanup=True, format='png')
            print("Visualization updated and displayed.")
        except graphviz.backend.execute.ExecutableNotFound:
            print("\nError: Graphviz executable not found!")
            print("Please make sure Graphviz is installed and its directory is in your system's PATH.")
            print("Download from: https://graphviz.org/download/")
        except Exception as e:
            print(f"An error occurred during rendering: {e}")

# --- مثال على الاستخدام ---

if __name__ == "__main__":
    # إنشاء شجرة بعقدة جذرية (action=1, info={'name': 'Start', 'type': 'root'})
    # المعرف الفريد الأول سيكون 0
    tree = VisualTree(1, {'name': 'Start', 'type': 'root'})
    print(f"Initial tree created with root (Action: 1, ID: {tree.root._id}).")
    root_id = tree.root._id # نحتفظ بمعرف الجذر إذا احتجناه

    # عرض الشجرة الابتدائية (ستكون فقط العقدة الجذرية بمعرف 0)
    tree.render_and_display()

    input("\nPress Enter to add initial nodes (Actions 2, 3, etc. - IDs will be 1, 2, ...)...")
    # إضافة بعض العقد بمعلومات مختلفة في القاموس info
    # سنحتفظ بـ IDs للعقد التي قد نريد حذفها لاحقاً
    child1_id = tree.add_node(1, 2, {'name': 'Action A', 'cost': 10}) # الابن الأول للجذر (action=2) - ID 1
    child2_id = tree.add_node(1, 3, {'name': 'Action B', 'description': 'Processing step'}) # الابن الثاني للجذر (action=3) - ID 2

    grandchild1_of_2_id = tree.add_node(2, 4, {'name': 'Sub-Action A1', 'status': 'completed'}) # ابن Action 2 (ID 1) (action=4) - ID 3
    grandchild2_of_2_id = tree.add_node(2, 5, {'name': 'Sub-Action A2', 'data_id': 'xyz123', 'flag': True}) # ابن Action 2 (ID 1) (action=5) - ID 4

    grandchild1_of_3_id = tree.add_node(3, 6, {'name': 'Sub-Action B1', 'progress': 0.5}) # ابن Action 3 (ID 2) (action=6) - ID 5

    # إضافة عقدتين لهما نفس الـ action (مثلاً action 4) ولكن آباء مختلفين
    duplicate_action_node1_id = tree.add_node(3, 4, {'name': 'Sub-Action B2 - Duplicate Action 4'}) # ابن Action 3 (ID 2) (action=4) - ID 6
    duplicate_action_node2_id = tree.add_node(4, 4, {'name': 'Sub-Action A1.1 - Duplicate Action 4'}) # ابن Action 4 (ID 3) (action=4) - ID 7

    # عرض الشجرة بعد الإضافات
    tree.render_and_display()

    print(f"\nAdded node with ID: {child1_id}, action 2")
    print(f"Added node with ID: {child2_id}, action 3")
    print(f"Added node with ID: {grandchild1_of_2_id}, action 4 (under action 2)")
    print(f"Added node with ID: {grandchild2_of_2_id}, action 5 (under action 2)")
    print(f"Added node with ID: {grandchild1_of_3_id}, action 6 (under action 3)")
    print(f"Added node with ID: {duplicate_action_node1_id}, action 4 (under action 3)")
    print(f"Added node with ID: {duplicate_action_node2_id}, action 4 (under action 4 ID={grandchild1_of_2_id})")


    input(f"\nPress Enter to remove node with ID {child1_id} (Action 2, and its subtree)...")
    # إزالة العقدة التي الـ ID الخاص بها هو child1_id (وهي العقدة التي action الخاص بها 2 تحت الجذر)
    # هذا سيؤدي أيضاً لإزالة أبنائها (IDs 3 و 4) وأبناء أبنائها (ID 7)
    tree.remove_node(child1_id)

    # عرض الشجرة بعد الحذف
    tree.render_and_display()


    input("\nPress Enter to try removing a non-existent node (ID 999)...")
    tree.remove_node(999) # محاولة إزالة عقدة غير موجودة بالـ ID
    tree.render_and_display() # عرض للتأكد أنه لم يحدث تغيير


    input(f"\nPress Enter to remove node with ID {duplicate_action_node1_id} (Action 4, under Action 3)...")
    # إزالة إحدى العقدتين اللتين لهما نفس الـ action 4، بالاعتماد على الـ ID الفريد الخاص بها
    tree.remove_node(duplicate_action_node1_id)

    # عرض الشجرة بعد الحذف
    tree.render_and_display()


    input("\nPress Enter to add another node (Action 7) under Action 3...")
    # هنا قد تكون هناك أكثر من عقدة بالـ action 3. الكود الحالي سيضيف تحت أول عقدة يجدها بـ action 3 (وهي العقدة ذات ID 2)
    tree.add_node(3, 7, {'name': 'Sub-Action B3', 'details': 'more info'})

    # عرض الشجرة بعد الإضافة الجديدة
    tree.render_and_display()


    input("\nPress Enter to try adding to a non-existent parent (Action 100)...")
    tree.add_node(100, 200, {'error': 'Should Fail'}) # محاولة الإضافة لأب غير موجود بالـ action
    tree.render_and_display() # عرض للتأكد أنه لم يحدث تغيير


    input("\nPress Enter to exit.")