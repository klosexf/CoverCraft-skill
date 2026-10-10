#!/usr/bin/env python3
"""Build an offline menu from generated samples or supplied screenshot regions."""
import argparse
import html
import json
import os
from pathlib import Path


def render_menu(skill_dir, output, recommendations=()):
    skill_dir=Path(skill_dir).resolve()
    output=Path(output).expanduser().resolve()
    if output.exists():
        raise ValueError('Output already exists; choose a new path: '+str(output))
    menu=json.loads((skill_dir/'assets/style-menu.json').read_text(encoding='utf-8'))
    samples={s['id']:s for s in json.loads((skill_dir/'assets/style-examples/manifest.json').read_text(encoding='utf-8'))['samples']}
    styles=menu['styles'];ids={s['id'] for s in styles};recommendations=list(recommendations)
    if len(recommendations)>3 or len(set(recommendations))!=len(recommendations) or not set(recommendations)<=ids:
        raise ValueError('Recommend up to three distinct valid style IDs')
    ranks={s:i for i,s in enumerate(recommendations)}
    styles=sorted(styles,key=lambda s:(ranks.get(s['id'],len(ranks)),s['id']))
    def local(path):return html.escape(Path(os.path.relpath(path,output.parent)).as_posix(),quote=True)
    cards=[]
    for s in styles:
        reference=s.get('source')=='user_reference'
        prompt_link=''
        if reference:
            image=thumbnail=skill_dir/s['reference_asset']
            from PIL import Image
            with Image.open(image) as original:
                width,height=original.size
            region=s['reference_region_xyxy']
            if len(region)!=4:
                raise ValueError('Reference region must have four coordinates for '+s['id'])
            x1,y1,x2,y2=region
            if not (0<=x1<x2<=width and 0<=y1<y2<=height):
                raise ValueError('Reference region outside source image for '+s['id'])
            # Clip the displayed source in CSS; do not modify or export source pixels.
            scale=min(180/(x2-x1),240/(y2-y1))
            viewport=f'width:{(x2-x1)*scale:.3f}px;height:{(y2-y1)*scale:.3f}px'
            placement=f'width:{width*scale:.3f}px;height:{height*scale:.3f}px;left:{-x1*scale:.3f}px;top:{-y1*scale:.3f}px'
            alt=html.escape(s['id']+' '+s['name']+' · 用户截图局部参考',quote=True)
            preview=f'<span class="reference-window" style="{viewport}"><img class="reference-image" style="{placement}" src="{local(image)}" alt="{alt}"></span>'
            sample_note='用户截图局部参考，非生成样张。支持横竖版与人物开关；人物/人形需服从本期选择。'
            original_label='查看整张来源截图'
        else:
            sample=samples[s['example_id']]
            image=skill_dir/'assets/style-examples'/sample['image']
            thumbnail=skill_dir/'assets/style-examples'/sample['thumbnail']
            alt=html.escape(s['id']+' '+s['name']+' · '+sample['headline'],quote=True)
            preview=f'<img src="{local(thumbnail)}" alt="{alt}">'
            people='原创人物' if sample['people']!='none' else '无人物'
            ratio='竖版' if sample['ratio']=='3:4' else '横版'
            sample_note=f'这张示例：{ratio} · {people}。此风格四种组合均可用。'
            original_label='查看原图'
            if sample.get('portable_prompt'):
                prompt=skill_dir/'assets/style-examples'/sample['portable_prompt']
                if not prompt.is_file():
                    raise ValueError('Portable prompt unavailable for '+s['id'])
                prompt_link=f' · <a href="{local(prompt)}">查看完整提示词</a>'
        if not image.is_file() or not thumbnail.is_file():
            raise ValueError('Sample image unavailable for '+s['id'])
        title=html.escape(s['name']);summary=html.escape(s['summary'])
        uses=html.escape('、'.join(s['suitable_for']))
        search=html.escape(' '.join([s['id'],s['name'],s['summary'],*s['suitable_for'],*s['tags'],*s.get('aliases',[])]),quote=True)
        badge='<span class="badge">本期推荐</span>' if s['id'] in ranks else '<span class="badge">截图参考</span>' if reference else ''
        cards.append(f'<article class="card" data-id="{s["id"]}" data-search="{search}" data-tags="{html.escape("|".join(s["tags"]),quote=True)}" data-selected="false"><a class="preview" href="{local(image)}" title="{original_label}">{preview}</a><div class="content"><div class="eyebrow"><span>{s["id"]} · 视觉风格</span>{badge}</div><h2>{title}</h2><p>{summary}</p><p>适合：{uses}</p><p class="sample">{sample_note}</p><a href="{local(image)}">{original_label}</a>{prompt_link}<button type="button" data-choose="{s["id"]}" data-name="{html.escape(s["name"],quote=True)}">选 {s["id"]} {title}</button></div></article>')
    note='本期优先推荐 '+ '、'.join(recommendations)+'；仍可以选择下面任意一种。' if recommendations else 'B01–B10 为基础风格，S01–S08 为截图提炼的特定风格；也可让 Agent 按内容决定。进阶分支不用额外选择。'
    page=(skill_dir/'assets/style-picker-template.html').read_text(encoding='utf-8')
    page=page.replace('__RECOMMENDATION_NOTE__',html.escape(note)).replace('__STYLE_CARDS__',''.join(cards))
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(page,encoding='utf-8')
    return dict(output=str(output),styles=len(styles),reference_styles=sum(s.get('source')=='user_reference' for s in styles),recommendations=recommendations,image_generation=False)


def main():
    skill=Path(__file__).resolve().parents[1]
    choices=[s['id'] for s in json.loads((skill/'assets/style-menu.json').read_text(encoding='utf-8'))['styles']]
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path,help='New HTML path; keep access to installed skill assets')
    parser.add_argument('--recommend',nargs='+',default=[],choices=choices,help='Up to three topic-specific B/S IDs')
    args=parser.parse_args()
    try:
        result=render_menu(skill,args.out,args.recommend)
    except (OSError,ValueError,KeyError) as exc:
        parser.exit(1,'Style preview failed: '+str(exc)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
