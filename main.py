from typing import List

from math import pow

reward_array = [1, 1, 1, 1, 1, 2, 3, 2, 4, 3]

class ResultCandidate:

    def __init__(self, seq, probabilitiesSum) -> None:
        """
        @param str seq - the sequence itself. Example: 0111010110. Guranteed to have length of 10 symbols
        @param probabilitiesSum - sum of probabilities for thsi sequence
        @param expectedValue - expected value for a given sequence 
        """
        self.probabilities_arr = [0.9, 0.91, 0.95, 0.97, 0.9, 0.8, 0.65, 0.75, 0.5, 0.55]
        self.seq = seq
        self.probabilitiesSum = probabilitiesSum 
        self.expectedValue = self.expected_value(seq)

    def expected_value(self, seq) -> float:

        global reward_array

        sum = 0.0

        for i in range(len(seq)):
            if seq[i] == '1':
                sum += reward_array[i] * self.probabilities_arr[i]
        
        return sum

class Solution:

    def __init__(self, time_probability_matrix) -> None:
        self.time_probability_matrix = time_probability_matrix
        self.target = self.requireTarget()        
        self.time_limit = self.requireTimeRange()
        self.probability_threshold = self.requireFloat("Введите пороговое значение alpha: ", 0.9)

    def prepare_bin(self, b) -> int:
        return b[2:]
    
    def toIntSafe(self, arg: any) -> int:
        try:
            return int(arg)
        except TypeError:
            print(f"Перданное значение '{arg}' не является integer-ом")
            exit(1)
    
    def requireFloat(self, text: str, default: float) -> float:
        try:
            raw = input(text)
            return float(raw)
        except ValueError:
            print(f"Перданное значение '{raw}' не является числом с плавающей точкой. Используется значение по-умолчанию : {default}")
            return default

    def requireInt(self, text: str, default: int) -> int:
        target = input(text)
        
        if target is None or len(target.strip()) == 0:
            return default
        
        return self.toIntSafe(target)

    def requireTarget(self) -> int:
        default = 12
        return self.requireInt(f"Введите пороговый балл ({default} по умолчанию): ", default)
    
    def requireTimeRange(self) -> int:
        time_limit = 3790
        return self.requireInt(f"Введите верхнею границу временного диапазона ({time_limit} по умолчанию): ", time_limit)     

    def checkTarget(self, binary: bin, target: int) -> bool:        
        sum = 0

        global reward_array

        for i in range(len(binary) - 1, -1, -1):
            if binary[i] == '1':
                task_index = len(reward_array) - (len(binary) - i)
                sum += reward_array[task_index]
        
        return sum >= target
    
    def zero_extend(self, s):
        while len(s) != 10:
            s = "0" + s
        else:
            return s

    def printResult(self, resiltCandidate: ResultCandidate) -> None:
        print(f"""
        Удоавлетворяющий сценарий: {self.zero_extend(resiltCandidate.seq)},
        Суммар вероятностей: {resiltCandidate.probabilitiesSum}
        Мат. Ожидание: {resiltCandidate.expectedValue}
        """)

    def deepCheck(
            self,
            binary,
            i,
            accumulatedTime: int, 
            accumulatedProbability : float
    ) -> None:
        """
        @param binary - the sequence itself. Example: 0111010110. Guranteed to have length of 10 symbols
        @param i - current index under investigation for a given sequence choosing given time expenses 
        @param accumulatedTime - accumulated time for a chosen time expenses (basically a sum of time for 
               all tasks for a given interation) 
        @param - accumulatedProbability - accumulated probability of this exact sequeqnce with these exact 
               time expenses to take place
        @return - probabilitiesSum - sum of probabilities of all sequences where the time spend fits the requirement
        """

        global reward_array 

        while i >= 0 and binary[i] != '1':
            i -= 1

        if i < 0:
            if self.time_limit >= accumulatedTime:
                return accumulatedProbability
            return 0.0

        task_index = len(reward_array) - (len(binary) - i)
        current_time_rpbability_matrix : dict = self.time_probability_matrix[task_index]

        success_probability = 0.0

        for time, probability in current_time_rpbability_matrix.items():
           success_probability += self.deepCheck(binary, i - 1, accumulatedTime + time, probability * accumulatedProbability)
        
        return success_probability

    def main(self):
        candidates : List[ResultCandidate] = []
        for n in range(0, int(pow(2, 10))):
            binary = self.prepare_bin(str(bin(n)))
            if self.checkTarget(binary, self.target):
                probabilitiesSum = self.deepCheck(binary, len(binary) - 1, 0, 1.0)
                if self.probability_threshold <= probabilitiesSum:
                    candidates.append(ResultCandidate(binary, probabilitiesSum))
        
        candidates.sort(key=lambda x: x.expectedValue, reverse=True)
        self.printResult(candidates[1])        

if __name__ == "__main__":
    Solution(
        [
            {
                60: 0.3,
                180: 0.5,
                300: 0.2
            },
            {
                75: 0.15,
                190: 0.6,
                330: 0.25
            },
            {
                60: 0.15,
                120: 0.35,
                250: 0.5
            },
            {
                130: 0.1,
                200: 0.3,
                350: 0.6
            },
            {
                75: 0.2,
                140: 0.45,
                210: 0.35
            },
            {
                200: 0.2,
                275: 0.35,
                380: 0.45
            },
            {
                310: 0.2,
                380: 0.4,
                450: 0.4
            },
            {
                200: 0.25,
                290: 0.4,
                370: 0.35
            },
            {
                380: 0.1,
                470: 0.25,
                650: 0.65
            },
            {
                150: 0.3,
                275: 0.55,
                500: 0.15
            }
        ]
    ).main()
