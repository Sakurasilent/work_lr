class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        https://leetcode.cn/problems/3sum-closest/description/?envType=problem-list-v2&envId=sorting
        """
        nums_len = len(nums)
        best = 10 ** 7
        nums.sort() # 排序
        def update(cur):
            nonlocal best
            if abs(cur - target) < abs(best-target):
                best = cur
            
        for index in range(nums_len):
            if index > 0 and nums[index] == nums[index - 1]:
                continue
            second = index + 1
            third = nums_len - 1
            while second < third:
                cur = nums[index] + nums[second] + nums[third]
                if cur == target:
                    return cur
                update(cur)
                if cur < target:
                    second += 1
                    while  second < third and nums[second] == nums[second - 1]:
                        second += 1
                else:
                    third -= 1
                    while second < third and nums[third] == nums[third + 1]:
                        third -= 1
                    # third -= 1
        return best 

if __name__ == "__main__":
    nums = [-1,2,1,-4]
    nums = [0,0,0,0]
    nums= [1,1,1,0]
    nums= [1,3,4,7,8,9]
    nums=[-4,2,2,3,3,3]
    target = 0
    fl = Solution()
    res = fl.threeSumClosest(nums=nums, target=target)
    print(res)
    pass