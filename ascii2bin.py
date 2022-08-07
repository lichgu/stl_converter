# Created by lcg at 21.07.22

import struct


def ascii2bin(in_path, out_path):
    try:
        with open(in_path, 'r') as f:
            data = f.read()

        w = open(out_path, 'wb')

        # 80 character header
        header, data = data.split('\n', 1)
        header.replace('solid', '')
        header = header[:80] if len(header) > 80 else header.ljust(80)
        w.write(bytearray(header.encode('ascii')))

        # prepare file content
        data = data.lower()
        for r in ['outer loop', 'endloop', 'endfacet']:
            data = data.replace(r, '')
        data = ' '.join(data.split())
        facets = data.split('facet')[1:]

        # number of facets stored in 4 byte little-endian unsigned integer
        w.write(struct.pack('<I', len(facets)))

        # iterating triangles
        for facet in data.split('facet')[1:]:
            partials = facet.split(' ')

            # normal vector
            normal_idx = partials.index('normal')
            w.write(struct.pack('<f', float(partials[normal_idx + 1])))
            w.write(struct.pack('<f', float(partials[normal_idx + 2])))
            w.write(struct.pack('<f', float(partials[normal_idx + 3])))

            # vertices
            vertex_idxs = [idx for idx, val in enumerate(partials) if val == 'vertex']
            for vertex_idx in vertex_idxs:
                w.write(struct.pack('<f', float(partials[vertex_idx + 1])))
                w.write(struct.pack('<f', float(partials[vertex_idx + 2])))
                w.write(struct.pack('<f', float(partials[vertex_idx + 3])))

            # 2-byte unsigned integer (zero in standard format)
            w.write(struct.pack('H', 0))

        w.close()

    except OSError as err:
        w.write(b'OSError for file {in_path}: {repr(err)}')
    except BaseException as err:
        w.write(f'Unexpected {type(err)}: {repr(err)}'.encode('ascii'))
    finally:
        w.close()
