from backend.LeetcodeQuestionService.db_mongo import questions_collection

questions = [
    {
        "id": 1,
        "title": "Two Sum",
        "question": "Complete the missing line in the Two Sum solution.",
        "code": "def twoSum(nums, target):\n    hashmap = {}\n    for i in range(len(nums)):\n        ### FILL HERE ###\n        hashmap[nums[i]] = i",
        "options": {
            "A": "if nums[i] in hashmap: return [i, hashmap[nums[i]]]",
            "B": "return [i, i + 1]",
            "C": "if target - nums[i] in hashmap: return [hashmap[target - nums[i]], i]",
            "D": "continue"
        },
        "correct_option": "C"
    },
    {
        "id": 2,
        "title": "Reverse Linked List",
        "question": "Fill in the missing line to reverse the linked list.",
        "code": "def reverseList(head):\n    prev = None\n    curr = head\n    while curr:\n        ### FILL HERE ###\n        curr = nxt\n    return prev",
        "options": {
            "A": "nxt = curr.next; curr.next = prev; prev = curr",
            "B": "prev = curr.next",
            "C": "nxt = prev",
            "D": "curr = prev.next"
        },
        "correct_option": "A"
    },
    {
        "id": 3,
        "title": "Valid Parentheses",
        "question": "Choose the correct condition to validate matching brackets.",
        "code": "def isValid(s):\n    stack = []\n    mapping = {')':'(', ']':'[', '}':'{'}\n    for c in s:\n        if c in mapping:\n            top = stack.pop() if stack else '#'\n            ### FILL HERE ###\n        else:\n            stack.append(c)\n    return not stack",
        "options": {
            "A": "if not stack: return False",
            "B": "if top != mapping[c]: return False",
            "C": "stack.append(c)",
            "D": "return True"
        },
        "correct_option": "B"
    },
    {
        "id": 4,
        "title": "Merge Two Sorted Lists",
        "question": "Select the line that merges nodes in sorted order.",
        "code": "def mergeTwoLists(l1, l2):\n    dummy = ListNode(0)\n    curr = dummy\n    while l1 and l2:\n        ### FILL HERE ###\n    curr.next = l1 if l1 else l2\n    return dummy.next",
        "options": {
            "A": "if l1.val <= l2.val: curr.next = l1; l1 = l1.next",
            "B": "curr.next = None",
            "C": "if l1 is None: break",
            "D": "l2 = l1.next"
        },
        "correct_option": "A"
    },
    {
        "id": 5,
        "title": "Binary Search",
        "question": "Choose the correct pointer movement for binary search.",
        "code": "def search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        ### FILL HERE ###\n    return -1",
        "options": {
            "A": "right = mid - 1 if target < nums[mid] else right",
            "B": "left = mid - 1",
            "C": "right = mid + 1",
            "D": "left = mid + 1 if target > nums[mid] else left; right = right"
        },
        "correct_option": "A"
    },
    {
        "id": 6,
        "title": "Climbing Stairs",
        "question": "Choose the recurrence relation for the DP solution.",
        "code": "def climbStairs(n):\n    if n <= 2: return n\n    dp = [0] * (n + 1)\n    dp[1], dp[2] = 1, 2\n    for i in range(3, n + 1):\n        ### FILL HERE ###\n    return dp[n]",
        "options": {
            "A": "dp[i] = dp[i - 1] + dp[i - 2]",
            "B": "dp[i] = dp[i] + dp[i - 1]",
            "C": "dp[i] = dp[i - 1]",
            "D": "dp[i] = dp[i - 3]"
        },
        "correct_option": "A"
    },
    {
        "id": 7,
        "title": "Maximum Subarray",
        "question": "Choose the Kadane update step.",
        "code": "def maxSubArray(nums):\n    curr = best = nums[0]\n    for n in nums[1:]:\n        ### FILL HERE ###\n        best = max(best, curr)\n    return best",
        "options": {
            "A": "curr = max(n, curr + n)",
            "B": "curr = curr - n",
            "C": "curr = n * curr",
            "D": "curr = 0"
        },
        "correct_option": "A"
    },
    {
        "id": 8,
        "title": "Best Time to Buy and Sell Stock",
        "question": "Fill in the logic to track minimum price and profit.",
        "code": "def maxProfit(prices):\n    min_price = float('inf')\n    max_profit = 0\n    for p in prices:\n        ### FILL HERE ###\n    return max_profit",
        "options": {
            "A": "min_price = min(min_price, p); max_profit = max(max_profit, p - min_price)",
            "B": "max_profit = p",
            "C": "p = min_price",
            "D": "min_price = max(min_price, p)"
        },
        "correct_option": "A"
    },
    {
        "id": 9,
        "title": "Number of Islands",
        "question": "Choose the line that marks a land cell as visited.",
        "code": "def dfs(grid, r, c):\n    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] == '0':\n        return\n    ### FILL HERE ###\n    dfs(grid, r+1, c)\n    dfs(grid, r-1, c)\n    dfs(grid, r, c+1)\n    dfs(grid, r, c-1)",
        "options": {
            "A": "grid[r][c] = '0'",
            "B": "return",
            "C": "grid[r][c] = '#'",
            "D": "grid = []"
        },
        "correct_option": "A"
    },
    {
        "id": 10,
        "title": "Longest Common Prefix",
        "question": "Fill in the condition that checks for a mismatch.",
        "code": "def longestCommonPrefix(strs):\n    if not strs: return \"\"\n    for j in range(len(strs[0])):\n        c = strs[0][j]\n        for i in range(1, len(strs)):\n            ### FILL HERE ###\n    return strs[0]",
        "options": {
            "A": "if j >= len(strs[i]) or strs[i][j] != c: return strs[0][:j]",
            "B": "return \"\"",
            "C": "continue",
            "D": "strs[i] = c"
        },
        "correct_option": "A"
    }
]

if questions_collection.count_documents({}) == 0:
    questions_collection.insert_many(questions)
    print("Inserted 10 LeetCode questions.")
else:
    print("Questions already exist. Skipping insert.")