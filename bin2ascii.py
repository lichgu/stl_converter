# Created by lcg at 21.07.22

import struct


def bin2ascii(in_path, out_path):
    try:
        with open(in_path, 'rb') as f:
            data = f.read()

        indent = '  '
        w = open(out_path, 'w')

        # 80 character header (replacement characters are removed)
        w.write('solid ')
        header = data[0:80]
        header = header.replace(b'\xEF\xBF\xBD', b'')
        w.write(header.decode('utf-8'))
        w.write('\n')

        # number of facets stored in 4 byte little-endian unsigned integer
        facet_count = struct.unpack('<I', data[80:84])[0]

        # iterating triangles
        # each described by twelve 32-bit floats + a 2 byte unsigned integer
        for i in range(facet_count):
            # normal vector
            w.write(f'{indent}facet normal ')
            normal_x = struct.unpack('f', data[84 + i * 50:88 + i * 50])[0]
            normal_y = struct.unpack('f', data[88 + i * 50:92 + i * 50])[0]
            normal_z = struct.unpack('f', data[92 + i * 50:96 + i * 50])[0]
            w.write(f'{normal_x} {normal_y} {normal_z}\n')

            # vertices
            w.write(f'{indent * 2}outer loop\n')
            for v in range(3):
                vertex_x = struct.unpack(
                    'f', data[96 + i * 50 + v * 12:100 + i * 50 + v * 12])[0]
                vertex_y = struct.unpack(
                    'f', data[100 + i * 50 + v * 12:104 + i * 50 + v * 12])[0]
                vertex_z = struct.unpack(
                    'f', data[104 + i * 50 + v * 12:108 + i * 50 + v * 12])[0]
                w.write(f'{indent * 3}vertex {vertex_x} {vertex_y} {vertex_z}\n')
            w.write(f'{indent * 2}endloop\n')

            w.write(f'{indent}endfacet\n')

        w.write(f'endsolid')

    except OSError as err:
        w.write(f'OSError for file {in_path}: {repr(err)}')
    except BaseException as err:
        w.write(f'Unexpected {type(err)}: {repr(err)}')
    finally:
        w.close()



