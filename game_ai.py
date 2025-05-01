from game_logic import State, ComputerPlayer # يفترض أن game_logic يوفر الفئات المطلوبة
from tree import VisualTree, Node
import math # لاستخدام math.inf

debug = True
def log(msg):
    if debug:
        print(msg)

class AiPlayer(ComputerPlayer):
    def __init__(self, level=2, name="Ai Player"):
        self.name = name
        self.my_player_number = None
        self.level = level
        self.depth = level + 2 # عمق الاستكشاف الأولي
        self.rows = 6
        self.cols = 7

    def get_player_action(self, state: State):
        """
        يحسب أفضل حركة باستخدام Minimax ويعرض شجرة الاستكشاف.
        """
        self.my_player_number = state.get_who_player_turn()

        # 1. تهيئة الشجرة المرئية
        # العقدة الجذرية تمثل الحالة الحالية قبل اتخاذ أي حركة من قبل AI.
        # الـ action للعقدة الجذرية يمكن أن يكون قيمة خاصة مثل -1 للإشارة إلى أنها الحالة الأولية.
        root_info = {
            'player_turn': self.my_player_number,
            'depth_level': self.depth,
            'state_type': 'Current' # وصف بسيط للحالة
        }
        treeObject = VisualTree(root_action=-1, root_info=root_info)
        root_node_id = treeObject.root._id

        log(f"Starting Minimax from root node ID: {root_node_id}")

        # 2. بدء استكشاف Minimax مع تمرير الشجرة ومعرف العقدة الحالية
        # Note: The initial call is for the maximizing player (the AI itself)
        best_score, best_action = self._minimax(
            treeObject,
            root_node_id, # معرف العقدة الحالية (الجذر)
            self.depth,
            True, # اللاعب الحالي هو اللاعب الأقصى (AI)
            state,
            alpha=float('-inf'),
            beta=float('inf')
        )

        log(f"Minimax finished. Best action: {best_action}, Best score: {best_score}")

        # 3. عرض الشجرة المرئية بعد انتهاء الاستكشاف
        treeObject.render_and_display()

        return best_action

    # تم تعديلها لتلقي كائن الشجرة ومعرف العقدة التي تمثل الحالة الحالية
    def _minimax(self, treeObject: VisualTree, current_node_id: int, depth: int, is_maximizing: bool, state: State, alpha: float, beta: float):
        """
        دالة Minimax التكرارية مع Alpha-Beta Pruning وبناء الشجرة المرئية.
        تمرر treeObject ومعرف العقدة الحالية التي تمثل 'state'.
        """
        # البحث عن العقدة الحالية في الشجرة المرئية لتحديث معلوماتها
        current_node = treeObject.find_node_by_id(current_node_id)
        if current_node is None:
            # هذا لا ينبغي أن يحدث إذا كانت المعرفات تمرر بشكل صحيح
            # log(f"Error: Current node with ID {current_node_id} not found in tree.") # إزالة الطباعة المزعجة
            # نرفع استثناء بدلاً من العودة بقيمة قد تكون خاطئة
            raise Exception(f"Error: Current node with ID {current_node_id} not found in tree during minimax.")

        # تحديث معلومات العقدة الحالية بقيم ألفا وبيتا الحالية عند دخول هذه الحالة
        current_node.info['player'] = "max player" if is_maximizing else "min player"
        current_node.info['alpha'] = alpha
        current_node.info['beta'] = beta
        current_node.info['is_maximizing'] = is_maximizing # إضافة لمن هو اللاعب لهذا الدور من الاستكشاف

        # قاعدة الاستدعاء التكراري (حالة نهائية أو وصول للعمق المطلوب)
        if state.is_terminate() or depth == 0:
            score = self._evaluate(state)
            # تحديث معلومات العقدة الحالية بالقيمة النهائية المحسوبة لها
            current_node.info['minimax_value'] = score
            if state.is_terminate():
                current_node.info['winner'] = state.get_winner_player_number()
            current_node.info['depth_reached'] = self.depth - depth # العمق من الجذر (0 هو الجذر)
            log(f"Node ID: {current_node_id}, Depth: {self.depth - depth}, Terminal/Depth 0. Evaluated Score: {score}")
            return score, None # لا يوجد إجراء "أفضل" من حالة طرفية / عند العمق النهائي

        # الحصول على الحركات المتاحة
        actions = state.get_available_actions()
        if not actions:
            # حالة لا يوجد فيها حركات متاحة ولكنها ليست حالة فوز/خسارة (مثلاً لوحة ممتلئة وتعادل)
            score = self._evaluate(state) # قيمة التعادل
            current_node.info['minimax_value'] = score
            current_node.info['no_actions'] = True
            current_node.info['depth_reached'] = self.depth - depth
            log(f"Node ID: {current_node_id}, Depth: {self.depth - depth}, No actions available. Evaluated Score: {score}")
            return score, None

        best_action = None

        # استكشاف الحالات المستقبلية
        if is_maximizing:
            best_score = float('-inf')
            for action in actions:
                # Alpha-Beta Pruning check BEFORE creating and exploring the child
                if beta <= alpha:
                    log(f"Pruning at node ID: {current_node_id}, Depth: {self.depth - depth}. Skipping further actions due to Alpha ({alpha}) vs Beta ({beta}).")
                    break # قص بقية الفروع

                # 3. بناء العقدة الابن في الشجرة المرئية قبل الاستدعاء التكراري
                child_info = {
                    # قيم ألفا وبيتا التي سيتم تمريرها للاستدعاء التالي
                    'alpha': alpha, # Note: This alpha is the one *before* this child is fully evaluated
                    'beta': beta, # Note: This beta is the one *before* this child is fully evaluated
                    'is_maximizing': not is_maximizing, # دور اللاعب في الحالة التي تم التوصل إليها
                    'depth_level': depth - 1,
                    'minimax_value': '?', # القيمة غير معروفة بعد، سيتم تحديثها لاحقاً
                }
                child_node = treeObject.add_node(current_node_id, action, child_info)

                if child_node is None:
                    # هذا لا ينبغي أن يحدث، لكن لضمان السلامة
                    # log(f"Error: Failed to add child node for action {action} under parent ID {current_node_id}") # إزالة الطباعة المزعجة
                    continue # تخطى هذا الفرع إذا لم يتمكن من إضافة العقدة

                # إنشاء الحالة الجديدة وتمرير معرف العقدة الابن في الاستدعاء التكراري
                new_state = state.take_action_in_different_state_object(action)
                # تمرير قيم ألفا وبيتا الحالية إلى الاستدعاء التالي
                score, _ = self._minimax(treeObject, child_node._id, depth - 1, False, new_state, alpha, beta)

                # 4. تحديث معلومات العقدة الابن بالقيمة التي عادت من الاستكشاف
                # child_node.info['minimax_value'] تم تحديثها بالفعل في الاستدعاء التكراري عند العودة من أبنائها أو الوصول لقاعدة الاستدعاء

                # تحديث أفضل نتيجة وحركة لهذا المستوى (Maximizing player)
                if score > best_score:
                    best_score = score
                    best_action = action
                # تحديث ألفا بعد تقييم هذا الفرع
                alpha = max(alpha, best_score)
                child_info['alpha'] = alpha


        else: # is_minimizing
            best_score = float('inf')
            for action in actions:
                # Alpha-Beta Pruning check BEFORE creating and exploring the child
                if beta <= alpha:
                    log(f"Pruning at node ID: {current_node_id}, Depth: {self.depth - depth}. Skipping further actions due to Alpha ({alpha}) vs Beta ({beta}).")
                    break # قص بقية الفروع

                # 3. بناء العقدة الابن في الشجرة المرئية
                child_info = {
                    # قيم ألفا وبيتا التي سيتم تمريرها للاستدعاء التالي
                    'alpha': alpha, # Note: This alpha is the one *before* this child is fully evaluated
                    'beta': beta, # Note: This beta is the one *before* this child is fully evaluated
                    'is_maximizing': not is_maximizing, # دور اللاعب في الحالة التي تم التوصل إليها
                    'depth_level': depth - 1,
                    'minimax_value': '?',
                }
                child_node = treeObject.add_node(current_node_id, action, child_info)

                if child_node is None:
                    # log(f"Error: Failed to add child node for action {action} under parent ID {current_node_id}") # إزالة الطباعة المزعجة
                    continue

                # إنشاء الحالة الجديدة وتمرير معرف العقدة الابن
                new_state = state.take_action_in_different_state_object(action)
                # تمرير قيم ألفا وبيتا الحالية إلى الاستدعاء التالي
                score, _ = self._minimax(treeObject, child_node._id, depth - 1, True, new_state, alpha, beta)

                # 4. تحديث معلومات العقدة الابن بالقيمة التي عادت
                # child_node.info['minimax_value'] تم تحديثها بالفعل

                # تحديث أفضل نتيجة وحركة لهذا المستوى (Minimizing player)
                if score < best_score:
                    best_score = score
                    best_action = action
                # تحديث بيتا بعد تقييم هذا الفرع
                beta = min(beta, best_score)


        # 5. تحديث معلومات العقدة الحالية بأفضل قيمة تم الحصول عليها من أبنائها
        # هذه القيمة هي قيمة minimax لهذه الحالة
        current_node.info['minimax_value'] = best_score
        current_node.info['depth_reached'] = self.depth - depth

        # يمكن إضافة أفضل حركة تم اختيارها من هذه العقدة كمعلومات إضافية
        # هذا مفيد بشكل خاص للعقد في مستوى الجذر والمستويات العليا
        if best_action is not None:
            current_node.info['chosen_action'] = best_action


        log(f"Node ID: {current_node_id}, Depth: {self.depth - depth}, Returning Score: {best_score}, Best Action from here: {best_action}")
        return best_score, best_action # نرجع أفضل score و action لهذا المستوى

    def _evaluate(self, state: State):
        """دالة التقييم لحالة اللوحة."""
        # تأكد أن التقييم صحيح حسب دور اللاعب الذي ينادي الدالة (self.my_player_number)
        if state.is_terminate():
            winner = state.get_winner_player_number()
            if winner == self.my_player_number:
                return float('inf') # فوز AI قيمة لا نهائية
            elif winner == 0: # تعادل
                return 0
            else: # فوز اللاعب الآخر
                return float('-inf') # خسارة AI قيمة سالبة لا نهائية

        # تقييم اللوحة للحالات غير النهائية
        board = state.get_board_as_list()
        score = 0
        opp_player = 3 - self.my_player_number # اللاعب الخصم هو 1 إذا كان AI 2، والعكس

        # تقييم مركز اللوحة
        center_col = self.cols // 2
        # نعطي قيمة أكبر لقطع اللاعب الحالي في العمود الأوسط
        center_count = sum(1 for r in range(self.rows) if board[r][center_col] == self.my_player_number)
        score += center_count * 3

        # تقييم النوافذ (4 قطع متجاورة) في الاتجاهات الأربعة
        for r in range(self.rows):
            for c in range(self.cols - 3):
                # أفقي
                window = [board[r][c + i] for i in range(4)]
                score += self._score_window(window, self.my_player_number, opp_player)

        for c in range(self.cols):
            for r in range(self.rows - 3):
                # رأسي
                window = [board[r + i][c] for i in range(4)]
                score += self._score_window(window, self.my_player_number, opp_player)

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                # قطري (من اليسار للأعلى إلى اليمين للأسفل)
                window = [board[r + i][c + i] for i in range(4)]
                score += self._score_window(window, self.my_player_number, opp_player)

        for r in range(self.rows - 3):
            for c in range(3, self.cols): # يبدأ من العمود 3 للقطر الآخر
                # قطري (من اليسار للأسفل إلى اليمين للأعلى)
                window = [board[r + i][c - i] for i in range(4)] # انتبه لطرح i من c
                score += self._score_window(window, self.my_player_number, opp_player)

        return score

    def _score_window(self, window, my_player, opp_player):
        """يقيّم نافذة بحجم 4 قطع."""
        score = 0
        count_self = window.count(my_player)
        count_opp = window.count(opp_player)
        count_empty = window.count(0)

        # نقاط للفوز أو الاقتراب من الفوز
        # لاحظ: حالات الفوز والخسارة النهائية يجب أن يتم التعامل معها بشكل أساسي
        # في دالة _evaluate لضمان القيم اللا نهائية في حالات الفوز/الخسارة الحقيقية
        if count_self == 4:
            score += 100 # قيمة عالية للفوز في هذه النافذة (هذه ليست قيمة لا نهائية حقيقية)
        elif count_self == 3 and count_empty == 1:
            score += 5 # فرصة جيدة للفوز
        elif count_self == 2 and count_empty == 2:
            score += 2 # فرصة محتملة

        # نقاط للخصم (نقاط سالبة لمنعه)
        if count_opp == 4:
            score -= 100 # قيمة منخفضة جداً لتجنب الخسارة في هذه النافذة
        elif count_opp == 3 and count_empty == 1:
            score -= 4 # منع الخصم من الفوز في الخطوة التالية

        return score