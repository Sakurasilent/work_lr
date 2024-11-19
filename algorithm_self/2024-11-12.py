class Solution(object):
    def threeSum(self, nums:list):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        https://leetcode.cn/problems/3sum/description/?envType=problem-list-v2&envId=sorting
        1. 进行排序
        2. 第一层遍历,不可出现与前一个数相同的数字
            1. index 大于1 要与前一个数比较是否相同
        3. 同时便利 index + 1 ---- len(data) 
            前后查找两个数使两数之和等于 -nums[index]
        """
        result = []
        # 1. sort
        nums.sort()
        for index in range(len(nums)):
            if index > 0 and nums[index]==nums[index-1]:
                continue
            index_seconde = index + 1
            index_third = len(nums) - 1
            while(index_seconde<index_third):
                if index_seconde != index+1 and nums[index_seconde] == nums[index_seconde - 1]:
                    index_seconde+=1
                    continue
                if index_third!=len(nums)-1 and nums[index_third]==nums[index_third + 1]:
                    index_third-=1
                    continue
                
                if nums[index_seconde]+nums[index_third] == -nums[index]:
                    result.append([nums[index], nums[index_seconde],nums[index_third]])
                    index_seconde += 1
                    index_third -= 1
                elif nums[index_seconde]+nums[index_third]>-nums[index]:
                    index_third-=1
                else:
                    index_seconde+=1
        return result


if __name__ == "__main__":
    nums=[4,5,1,2,3,-3,-1,0,0]
    fl = Solution()
    res = fl.threeSum(nums=nums)
    print(res)
    pass