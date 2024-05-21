import numpy as np
import cv2

class Cell:
    def __init__(self,start_row, end_row, start_col, end_col, points,content):
        self.start_row = int(start_row)
        self.end_row = int(end_row)
        self.start_col = int(start_col)
        self.end_col = int(end_col)
        self.content = content

        points = points.split(' ')
        new_points = []
        for p in points:
            p = p.split(',')
            new_points.append(np.array([int(p[0]), int(p[1])]))
        if len(new_points) > 4:
            # 计算多边形最小外接矩形
            new_points = self.get_minarea_rect(new_points)

        self.points = np.array(new_points)


    def get_minarea_rect(self, points):
        bounding_box = cv2.minAreaRect(np.array(points).astype(np.int32))
        points = sorted(list(cv2.boxPoints(bounding_box)), key=lambda x: x[0])
        points = np.array(points, dtype=np.int32)

        index_a, index_b, index_c, index_d = 0, 1, 2, 3
        if points[1][1] > points[0][1]:
            index_a = 0
            index_d = 1
        else:
            index_a = 1
            index_d = 0
        if points[3][1] > points[2][1]:
            index_b = 2
            index_c = 3
        else:
            index_b = 3
            index_c = 2

        box = [points[index_a], points[index_b], points[index_c], points[index_d]]
        return box

    def __str__(self):
        return 'start_row:{}, end_row:{}, start_col:{}, end_col:{}'.format(self.start_row, self.end_row, self.start_col, self.end_col)
    
    def get_html_cell(self):
        return '<td rowspan="{}" colspan="{}">{}</td>'.format(self.end_row - self.start_row + 1, self.end_col - self.start_col + 1, self.content)
    
    def get_html_label(self):
        cell_label = []
        if self.start_row == self.end_row:
            if self.start_col == self.end_col:
                cell_label.append('<td>')
                cell_label.append('</td>')
            else:
                cell_label.append('<td')
                cell_label.append(' colspan="{}"'.format(self.end_col - self.start_col + 1))
                cell_label.append('>')
                cell_label.append('</td>')
        else:
            if self.start_col == self.end_col:
                cell_label.append('<td')
                cell_label.append(' rowspan="{}"'.format(self.end_row - self.start_row + 1))
                cell_label.append('>')
                cell_label.append('</td>')
            else:
                cell_label.append('<td')
                cell_label.append(' rowspan="{}" colspan="{}"'.format(self.end_row - self.start_row + 1, self.end_col - self.start_col + 1))
                cell_label.append('>')
                cell_label.append('</td>')
        return cell_label
    
    def get_points(self):
        return self.points.tolist()

    
class Table:
    def __init__(self, cells):
        self.cells = cells
        # 对cells进行排序 按照start_row从小到大，start_col从小到大排序
        self.cells = sorted(self.cells, key=lambda x: (x.start_row, x.start_col))
        self.max_row = self.cells[-1].end_row
        self.max_col = self.cells[-1].end_col
    

    def recorvery_html_table(self):
        result_html = '<html>\n<body>\n'
        result_html += '<table border="1">\n' 
        result_html += '<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />'
        for i in range(self.max_row):
            result_html += '<tr>\n'
            for j in range(self.max_col):
                for cell in self.cells:
                    if cell.start_row == i and cell.start_col == j:
                        result_html += cell.get_html_cell()
            result_html += '</tr>\n'

        result_html += '</table>\n</body>\n</html>'

        return result_html
    
    def get_html_label(self):
        html_label = {}
        structure = {}
        structure_tokens = []
        cells = []
        structure_tokens.append('<tbody>')
        for i in range(self.max_row):
            structure_tokens.append('<tr>')
            for j in range(self.max_col):
                for cell in self.cells:
                    if cell.start_row == i and cell.start_col == j:
                        structure_tokens.extend(cell.get_html_label())
                        cell_dict = {}
                        cell_dict['bbox'] = cell.get_points()
                        cell_dict['tokens'] = cell.content
                        cells.append(cell_dict)
            structure_tokens.append('</tr>')

        structure_tokens.append('</tbody>')
        
        # 组装label信息
        structure['tokens'] = structure_tokens
        html_label['structure'] = structure
        html_label['cells'] = cells

        return html_label
