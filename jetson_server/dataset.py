# 匯入所需的庫和模組
import torch
import torch.utils.data
import glob
import PIL.Image
import subprocess
import cv2
import os
import uuid
import subprocess

# 定義圖像分類數據集的類別
class ImageClassificationDataset(torch.utils.data.Dataset):
    
    def __init__(self, directory, categories, transform=None):
        self.categories = categories  # 數據集的類別列表
        self.directory = directory    # 數據集的目錄路徑
        self.transform = transform    # 資料轉換函數
        self._refresh()               # 初始化時刷新數據集

    def __len__(self):
        return len(self.annotations)  # 返回數據集的樣本數

    def __getitem__(self, idx):
        ann = self.annotations[idx]  # 獲取指定索引的數據樣本
        image = cv2.imread(ann['image_path'], cv2.IMREAD_COLOR)  # 讀取圖像
        image = PIL.Image.fromarray(image)  # 將圖像轉換為PIL.Image對象
        if self.transform is not None:
            image = self.transform(image)  # 使用轉換函數對圖像進行處理
        return image, ann['category_index']  # 返回處理後的圖像和類別索引

    def _refresh(self):
        self.annotations = []  # 初始化樣本列表
        for category in self.categories:
            category_index = self.categories.index(category)
            for image_path in glob.glob(os.path.join(self.directory, category, '*.jpg')):
                # 遍歷目錄中的圖像文件，並記錄每個樣本的路徑和類別信息
                self.annotations += [{
                    'image_path': image_path,
                    'category_index': category_index,
                    'category': category
                }]

    def save_entry(self, image, category):
        """將BGR8格式的圖像保存到數據集的指定類別中"""
        if category not in self.categories:
            raise KeyError('在該數據集中找不到名為%s的類別。' % category)
            
        filename = str(uuid.uuid1()) + '.jpg'
        category_directory = os.path.join(self.directory, category)
        
        if not os.path.exists(category_directory):
            subprocess.call(['mkdir', '-p', category_directory])
            
        image_path = os.path.join(category_directory, filename)
        cv2.imwrite(image_path, image)  # 將圖像保存到指定類別的目錄中
        self._refresh()  # 刷新數據集以反映新的樣本
        return image_path

    def get_count(self, category):
        count = 0
        for a in self.annotations:
            if a['category'] == category:
                count += 1
        return count
