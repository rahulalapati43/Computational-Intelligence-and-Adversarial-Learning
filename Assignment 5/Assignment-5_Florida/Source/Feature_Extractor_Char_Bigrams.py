import os
import optparse
import operator
import math
from collections import OrderedDict

#defining the way i want to capture user input
parser = optparse.OptionParser()
parser.add_option('--writing_samples',dest='writing_samples',
                  default='',#default empty!
                  help='location of writing samples')
parser.add_option('--dataset_type',dest='dataset_type',
                  default='',#default empty!
                  help='CASIS-25 or SEC-SportsWriters')
parser.add_option('--feature_files',dest='feature_files',
                  default='',#default empty!
                  help='location to store raw feature file')
parser.add_option('--normalized_feature_files',dest='normalized_feature_files',
                  default='',#default empty!
                  help='location to store normalized feature file')

(options,args) = parser.parse_args()

#assigning the user input
writing_samples = options.writing_samples
dataset_type = options.dataset_type
feature_files = options.feature_files
normalized_feature_files = options.normalized_feature_files

#files (writing samples) inside the directory
writing_samples_files = os.listdir(writing_samples)

#ASCII order 32 to 126 : count 95
keys = []
for x in range(65,127):
    for y in range(65,127):
        key = chr(x).lower() + chr(y).lower()
        if key not in keys:
            keys.append(key)

#output files for term frequencies and normalized feature vectors
raw_fv_file = open(feature_files,'w+')
normalized_fv_file = open(normalized_feature_files, 'w+')

# #initializing a dictionary with keys as ASCII order 32 to 126 and their values as 0.0
# raw_fv_dict = OrderedDict.fromkeys(keys,0.0)
#
# for file in writing_samples_files:
#     print file
#     writing_sample = open(writing_samples + "/" + file,'r')
#     #getting the character count
#     for line in writing_sample:
#         for char in line:
#             for char_in in line:
#                 bigram_key = char.lower() + char_in.lower()
#                 if bigram_key in keys:
#                     raw_fv_dict[bigram_key] += 1
#     writing_sample.close()
#
# sorted_list = sorted(raw_fv_dict.items(),key=operator.itemgetter(1),reverse=True)
#
# sort_keys = []
# for tuple in sorted_list:
#     if tuple[1] > 0.0:
#         sort_keys.append(tuple[0])
#
# print sort_keys

sort_keys = ['ee', 'et', 'te', 'ae', 'ea', 'tt', 'eo', 'oe', 'en', 'ne', 'at', 'ta', 'es', 'se', 'aa', 'ei', 'ie', 'er', 're', 'ot', 'to', 'nt', 'tn', 'ao', 'oa', 'st', 'ts', 'an', 'na', 'eh', 'he',
 'it', 'ti', 'oo', 'as', 'sa', 'rt', 'tr', 'ai', 'ia', 'nn', 'de', 'ed', 'no', 'on', 'ar', 'ra', 'el', 'le', 'os', 'so', 'ss', 'ht', 'th', 'ns', 'sn', 'io', 'oi', 'in', 'ni', 'or', 'ro',
 'nr', 'rn', 'ah', 'ha', 'ii', 'is', 'si', 'dt', 'td', 'rs', 'sr', 'rr', 'ad', 'da', 'lt', 'tl', 'ir', 'ri', 'ho', 'oh', 'al', 'la', 'hn', 'nh', 'ef', 'fe', 'do', 'od', 'eu', 'ue', 'hs',
 'sh', 'dn', 'nd', 'ce', 'ec', 'hi', 'ih', 'lo', 'ol', 'hr', 'rh', 'ds', 'sd', 'ln', 'nl', 'eg', 'ge', 'di', 'id', 'dr', 'rd', 'ls', 'sl', 'hh', 'em', 'me', 'ft', 'tf', 'il', 'li', 'tu',
 'ut', 'ew', 'we', 'af', 'fa', 'ct', 'tc', 'lr', 'rl', 'au', 'ua', 'ac', 'ca', 'dd', 'gt', 'tg', 'dh', 'hd', 'fo', 'of', 'ep', 'pe', 'ag', 'ga', 'ou', 'uo', 'hl', 'lh', 'mt', 'tm', 'fn',
 'nf', 'll', 'nu', 'un', 'tw', 'wt', 'co', 'oc', 'ey', 'ye', 'cn', 'nc', 'am', 'ma', 'fs', 'sf', 'dl', 'ld', 'su', 'us', 'aw', 'wa', 'go', 'og', 'cs', 'sc', 'fi', 'if', 'fr', 'rf', 'gn',
 'ng', 'iu', 'ui', 'ru', 'ur', 'ci', 'ic', 'pt', 'tp', 'be', 'eb', 'cr', 'rc', 'mo', 'om', 'gs', 'sg', 'ow', 'wo', 'gi', 'ig', 'ty', 'yt', 'ap', 'pa', 'mn', 'nm', 'nw', 'wn', 'ms', 'sm',
 'ay', 'ya', 'ek', 'ke', 'gr', 'rg', 'im', 'mi', 'fh', 'hf', 'hu', 'uh', 'sw', 'ws', 'iw', 'wi', 'op', 'po', 'ch', 'hc', 'df', 'fd', 'du', 'ud', 'bt', 'tb', 'mr', 'rm', 'np', 'pn', 'rw',
 'wr', 'cd', 'dc', 'gh', 'hg', 'oy', 'yo', 'ab', 'ba', 'ps', 'sp', 'fl', 'lf', 'lu', 'ul', 'ny', 'yn', 'ev', 've', 'ip', 'pi', 'kt', 'tk', 'cl', 'lc', 'hm', 'mh', 'sy', 'ys', 'pr', 'rp',
 'dg', 'gd', 'ak', 'ka', 'hw', 'wh', 'iy', 'yi', 'gl', 'lg', 'bo', 'ob', 'ry', 'yr', 'ff', 'dm', 'md', 'bn', 'nb', 'dw', 'wd', 'uu', 'lm', 'ml', 'bs', 'sb', 'ko', 'ok', 'hp', 'ph', 'tv',
 'vt', 'cc', 'lw', 'wl', 'kn', 'nk', 'bi', 'ib', 'av', 'va', 'br', 'rb', 'hy', 'yh', 'dp', 'pd', 'ks', 'sk', 'fu', 'uf', 'cu', 'uc', 'cf', 'fc', 'dy', 'yd', 'lp', 'pl', 'ik', 'ki', 'kr',
 'rk', 'gg', 'ov', 'vo', 'ly', 'yl', 'gu', 'ug', 'nv', 'vn', 'fg', 'gf', 'bh', 'hb', 'mm', 'sv', 'vs', 'cg', 'gc', 'iv', 'vi', 'bd', 'db', 'fm', 'mf', 'mu', 'um', 'cm', 'mc', 'hk', 'kh',
 'ww', 'bl', 'lb', 'rv', 'vr', 'fw', 'wf', 'uw', 'wu', 'cw', 'dk', 'kd', 'wc', 'gm', 'mg', 'gw', 'wg', 'fp', 'pf', 'kl', 'lk', 'pu', 'up', 'uy', 'yu', 'cp', 'pc', 'hv', 'vh', 'mw', 'wm',
 'fy', 'yf', 'cy', 'yc', 'dv', 'vd', 'pp', 'gp', 'pg', 'gy', 'yg', 'bu', 'ub', 'lv', 'vl', 'mp', 'pm', 'bf', 'fb', 'yy', 'bc', 'cb', 'ej', 'je', 'pw', 'wp', 'wy', 'yw', 'my', 'ym', 'fk',
 'kf', 'ck', 'kc', 'ku', 'uk', 'bg', 'gb', 'py', 'yp', 'bm', 'mb', 'gk', 'kg', 'bw', 'wb', 'jt', 'tj', 'fv', 'vf', 'bb', 'kw', 'wk', 'aj', 'ja', 'km', 'mk', 'uv', 'vu', 'cv', 'vc', 'bp',
 'pb', 'by', 'yb', 'kk', 'gv', 'vg', 'jo', 'oj', 'jn', 'nj', 'kp', 'pk', 'js', 'sj', 'mv', 'vm', 'ky', 'yk', 'jr', 'rj', 'vw', 'wv', 'ij', 'ji', 'bk', 'kb', 'eq', 'qe', 'pv', 'vp', 'ex',
 'xe', 'vy', 'yv', 'vv', 'hj', 'jh', 'qt', 'tq', 'dj', 'jd', 'aq', 'qa', 'tx', 'xt', 'bv', 'vb', 'jl', 'lj', 'ax', 'xa', 'kv', 'vk', 'nq', 'qn', 'qr', 'rq', 'oq', 'qo', 'ox', 'xo', 'nx',
 'xn', 'qs', 'sq', 'ez', 'ze', 'iq', 'qi', 'sx', 'xs', 'ju', 'uj', 'cj', 'jc', 'fj', 'jf', 'ix', 'xi', 'rx', 'xr', 'hq', 'qh', 'gj', 'jg', 'dq', 'qd', 'tz', 'zt', 'az', 'za', 'hx', 'xh',
 'jm', 'mj', 'jw', 'wj', 'dx', 'xd', 'lq', 'ql', 'nz', 'zn', 'lx', 'xl', 'jp', 'pj', 'oz', 'zo', 'jy', 'yj', 'qu', 'uq', 'fq', 'qf', 'bj', 'jb', 'rz', 'zr', 'sz', 'zs', 'iz', 'zi', 'cq',
 'qc', 'jk', 'kj', 'dz', 'zd', 'ux', 'xu', 'hz', 'zh', 'fx', 'xf', 'cx', 'xc', 'gq', 'qg', 'lz', 'zl', 'gx', 'xg', 'wx', 'xw', 'jv', 'vj', 'mx', 'xm', 'jj', 'qw', 'wq', 'mq', 'qm', 'pq',
 'qp', 'px', 'xp', 'uz', 'zu', 'fz', 'zf', 'bq', 'qb', 'kq', 'qk', 'qy', 'yq', 'xy', 'yx', 'cz', 'zc', 'bx', 'xb', 'gz', 'zg', 'mz', 'zm', 'kx', 'xk', 'pz', 'zp', 'wz', 'zw', 'qv', 'vq',
 'vx', 'xv', 'bz', 'zb', 'yz', 'zy', 'qq', 'xx', 'kz', 'zk', 'vz', 'zv', 'zz', 'jq', 'qj', 'jx', 'xj', 'e[', 'e]', '[e', ']e', 'jz', 'zj', 'qz', 'zq', 'qx', 'xq', 'n[', 'n]', 't[', 't]',
 '[n', '[t', ']n', ']t', 'a[', 'a]', '[a', ']a', 'o[', 'o]', '[o', ']o', 's[', 's]', '[s', ']s', 'i[', 'i]', '[i', ']i', 'g[', 'g]', 'h[', 'h]', '[g', '[h', ']g', ']h', 'r[', 'r]', '[r',
 ']r', 'xz', 'zx', 'm[', 'm]', '[m', ']m', 'w[', 'w]', '[w', ']w', 'd[', 'd]', '[d', ']d', 'l[', 'l]', 'u[', 'u]', '[l', '[u', ']l', ']u', 'y[', 'y]', '[y', ']y', 'c[', 'c]', '[c', ']c',
 'f[', 'f]', 'v[', 'v]', '[f', '[v', ']f', ']v', '[[', '[]', '][', ']]', 'k[', 'k]', 'p[', 'p]', '[k', '[p', ']k', ']p', 'b[', 'b]', '[b', ']b', 'x[', 'x]', '[x', ']x']

for file in writing_samples_files:
    print file
    sorted_fv_dict = OrderedDict.fromkeys(sort_keys, 0.0)
    writing_sample = open(writing_samples + "/" + file,'r')
    #getting the character count
    for line in writing_sample:
        for char in line:
            for char_in in line:
                bigram_key = char.lower() + char_in.lower()
                if bigram_key in sort_keys:
                    sorted_fv_dict[bigram_key] += 1
    writing_sample.close()

    #getting the file name to append it to the begining of the line
    if (dataset_type == "CASIS-25"):
        file = file.split('_')
        raw_fv_file.write(file[0] + ',')
        normalized_fv_file.write(file[0] + ',')
    elif (dataset_type == "SEC-SportsWriters"):
        file = file.split('_')
        raw_fv_file.write(file[1] + ',')
        normalized_fv_file.write(file[1] + ',')

    #getting the term frequencies per file
    values = sorted_fv_dict.values()

    #calculating magnititude
    squared_sum = 0
    for value in values:
        squared_sum += math.pow((value - 0), 2)

    magnititude = math.sqrt(squared_sum)

    #getting the normalized feature vectors
    for value in range(0,len(values)-1):
        raw_fv_file.write(str(values[value]) + ',')
        normalized_fv_file.write(str(values[value]/magnititude) + ',')

    raw_fv_file.write(str(values[len(values)-1]) + '\n')
    normalized_fv_file.write(str(values[len(values)-1]/magnititude) + '\n')

raw_fv_file.close()
normalized_fv_file.close()