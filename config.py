# coding=utf8
# author=PlatinumGod
# created on 

patterns = [
    ['<span class="description unfold-item">\n<span class="content">(.*?)</span>', False, 'RESULTdescrption'],
    ['</span><strong>(\d+)</strong>赞同</span>', True, 'RESULT赞同'],
    ['</span><strong>(\d+)</strong>感谢</span>', True, 'RESULT感谢'],
    ['提问\n<span class="num">(\d+)</span>', True, 'RESULT提问'],
    ['回答\n<span class="num">(\d+)</span>', True, 'RESULT回答'],
    ['文章\n<span class="num">(\d+)</span>', True, 'RESULT文章'],
    ['收藏\n<span class="num">(\d+)</span>', True, 'RESULT收藏'],
    ['公共编辑\n<span class="num">(\d+)</span>', True, 'RESULT公共编辑'],
    ['<div class="zm-profile-section-item zm-item clearfix".*?</button>\n</div>\n</div>\n</div>\n</div>', False, 'RESULT最近动态']
]

createtask = {
    'a': 'n'
}