import pytest
import random

from binascii import hexlify, unhexlify

from tumblebit.rsa import RSA
from tumblebit.crypto import chacha
from tumblebit.puzzle_solver import PuzzleSolverClient, PuzzleSolverServer, Puzzle_Solver
import tumblebit


def predictableRandomness(bits):
    return random.getrandbits(bits).to_bytes(int(bits/8), byteorder='big')

Puzzle_Solver.compute_rand = staticmethod(predictableRandomness)



class TestPuzzleSolver():
    def test_puzzle_solver_complete(self):
        random.seed(1)

        server_keys = RSA(u"tests/test_data/server_keys", "test")
        server_keys.load_public_key()
        server_keys.load_private_key()

        server_pubkey = RSA(u"tests/test_data/server_keys", "test")
        server_pubkey.load_public_key()


        epsilon = b"828134975835142c2062b33020e5b360bb8af6ceb137715ba95dc901f406970c34931500f93f4b73647691d1b4d7ca7fb1256e4aa3b56c90a42c9be263c76101d0df812b1b9cab0c7eae2e577c22ce2896edfc30c2f40002e4a37c682a7b2f8ffb8afa7afd24cca0764be74cda664a40f55940bed0ebe4f20f59f0038fd50eb3e8d19f0e2a90580eef3a549bd1111e077b1c88db171b8fa2297e75d9986b0316db71e239d4b5e0c01f5849a2ac0726a0dfdcd577c7ec96d3b4f10bdcabb3bf8596b5a34cb7e032f090c5eb078c9efc59cd5f14309ee09e565a74ca48af27db32d817733ad2bd91bbee802147cfa4efd1b113d59d8430094d2e33d08c6d3b10b5"
        
        puzzle = server_keys.encrypt(unhexlify(epsilon))

        expected_puzzle = b"70e0a26c87f905a5d800eef677e055d0699a186682cbed9adde01d478f92a2abeff5d115a8ac54f78b52774f428f056887d0daea9d6c59069c5ee22985a9cc273bd57dee73ed0bebeb5f93b910fd170cae9f33b38c82a7db48b3a8c545db2bb10857f6ba316501cb6c24afda26d2869b43b98378eaef0c57019069ccbfd0e970e63d01e15a71c3949ff8373be1c38e50f2c8f6b96e6bfe6a342205ec3710d80b0506ee13798e435f7b55e9465748abcc77d316b0a1a45d7b9b239011a3b409608cf9eb909189a47f4466e368f7e33b0890975479f1182c640af588194d694f0aaa3b889ed9f9202c89926d1e2e18e2d2a9915569a332f39ae68391abe9eb6ed8"
        assert hexlify(puzzle) == expected_puzzle

        client = PuzzleSolverClient(server_pubkey, puzzle)
        server = PuzzleSolverServer(server_keys)

        puzzles = client.prepare_puzzle_set(puzzle)

        assert puzzles is not None
        expected_num_puzzles = 300
        assert len(puzzles) == expected_num_puzzles
        assert puzzles[0] == b'\xa6F\x87\xbf\xcbA`\xd7\xdd\xe9p\x8c\xdb\x16?\xf1\x1d\x9e\x1e~M/$\xb0\xda\xeb-.&U@\xa2\n\x9f]5\xc3\x1d?m\x91\xfa\xad\xff\x9c\x07\xa0\xbbb\xb1\x9e\x04\xf97r\xb1<\xef\xacD[z\xa0\x18\xaf\xa8\xb9\xee\xee\xab\xe0u\xfe\x06\x1dH\xe1Gw\xee\x03\xb2\xb1\xd0\x0b\xa8`8\xb1\xbb9\xd7\x8fL\x95\x02_\xda\xd1\xc1k\xbd6\x92\x11\xdc$\xf4p\x05^J(\x9d\xd2\x9f\x1d\x92\x99\xa5Y\xdcKa+D\xf6\xfd\xad\xf9^\xc6ceW\x9e;\x92P\xec\xd6\x07H\xb4\xe8\x13g\xc4!\x17\xb1\xad\xb3\x95\xab+jh>\x86Wq+\\\xe5kTRu;ts\x06IW\xc9\x17w\x94*\xfa\xc0\x15\x98\xdb\xac2\x8bf\x00eO\xe5\r-R\xdb\xbd\xf7n\xd3\xd7\x9c\xcfX\xa4\x06\xbc\xa9k\xcfjh\x95+Q,z\xa6\x10\xda+\x15ESC\xda\t\xb4 y\xf7\x81\x8b\x19-\xdex\x0e\xb9\x0elO\x84\xd7\x8b\xd8\x03\xec\xd0Q\x0b\xe9\x12\xcaM'
        assert puzzles[1] == b'q^\x1fg|y5-\x1ej\xdc\xec,t\x9a.\xae\xfb4\x0c6\xb1Ek\x12\x17\xf1\x19\xd88\x03^\xdc\x9bW\x97\xbf\xb1\xf11\x0b\x9d#\xf6\x94\x93\xe6\xda\xa1\x19M\xf8p\r\xd1\x15\x14\x16\x98\xf2\xb2\x88\x80\x92\x81H\r\xb2\xbd!`\xc8[e=\xd0W]\xbe\xae\xba\xabe\xc02\xa0Za\x17\x11\xe3\xf4\xc8\xab\xfef\xe8\xd5\xd6\x87)\xc8\xf4N\xfcl\x06\x1a\xf3f\x91Zb_\xef\x98b\x8e\xf0\x81\xe3O\x8c\x12K"\x13N\x94\xcc\x85\x101\xc6O\xa9t\xd2\x7f\xd9Qn\x97\x10\xd9\xd0\x80\xadL4^\xaf`\xef\xa7\xaa\xd5Ig\x11\x83q\xf2\xfff\x96\x1c\xcc\x9fTw\x86\x83\xfc)\xfc(\xea\xa0\xd2=\xed\xf6u\xf5[P\x8ab\xa4\xd1\xeb\n\xb9\xb3U\xeah\xfcU\x034l/\xda\xbc/R\x1b\x01\xd9\xeaV\x93\x8b\xaf\x84\x17\x18vn\xa5]a\x1f\xf7\x08\x15\xb5G\x1e\x1dJ\xb7\\\x02F\x1e\xe9>\xa6{$\xf6-g\xe3\x11\xea\x1eX\xce\x17C\xb0:'

        assert client.F == [223, 142, 32, 90, 117, 45, 198, 267, 67, 54, 146, 159, 244, 135, 213, 152, 274, 113, 179, 34, 97, 1, 18, 202, 197, 228, 95, 219, 214, 91, 108, 92, 225, 220, 29, 161, 296, 15, 48, 236, 88, 121, 157, 230, 72, 100, 191, 124, 42, 130, 71, 281, 216, 182, 39, 55, 260, 208, 248, 69, 166, 66, 165, 119, 155, 123, 242, 196, 44, 136, 87, 195, 253, 26, 194, 203, 150, 176, 175, 192, 115, 263, 261, 272, 232, 70, 279, 162, 73, 204, 22, 107, 98, 0, 200, 266, 186, 289, 297, 50, 240, 206, 153, 264, 30, 255, 273, 125, 33, 86, 190, 282, 84, 82, 177, 231, 226, 104, 249, 27, 12, 126, 284, 19, 94, 209, 120, 251, 250, 81, 85, 147, 164, 229, 3, 154, 178, 288, 207, 111, 184, 193, 262, 139, 60, 17, 137, 239, 28, 156, 76, 163, 10, 160, 132, 270, 20, 41, 256, 105, 114, 215, 276, 217, 271, 280, 58, 235, 122, 172, 143, 65, 5, 158, 31, 77, 295, 96, 35, 23, 173, 103, 89, 205, 21, 245, 101, 167, 265, 40, 275, 49, 258, 46, 283, 185, 291, 110, 106, 212, 37, 151, 47, 116, 180, 6, 278, 16, 294, 188, 285, 99, 102, 247, 168, 233, 237, 80, 252, 138, 169, 257, 243, 145, 68, 4, 2, 174, 141, 59, 221, 11, 93, 269, 149, 36, 224, 131, 24, 211, 14, 109, 52, 38, 129, 127, 128, 63, 61, 118, 7, 133, 292, 170, 112, 144, 246, 83, 53, 62, 290, 187, 218, 75, 183, 238, 74, 171, 78, 140, 57, 43, 241, 181, 254, 199, 148, 134, 227, 234, 64, 268, 287, 210, 277]
        assert client.fake_blinds[0] == b'\xea\xf5\xc03\xa5\xcd\x95\xe7\x1c\xf3\xd1y~\x07P\xea\x92HA\x94\xae\xf4%\x9c\xbb+\x92\xc3\xc8xh\xfaV\xe0\xa2Ff?B;\x8a\x0fB\x83N\x07Q\xd7Y\xa7\x8b\x13s\x15\xd9i\xb7\xcc\xbaXq;\x83\x1b\x1f\xb7\xf6(\x007\\\rR\xdd4\xd6\x87D\xd3\xc0\xc24G/[Xyj\xada\x1a>\x80\xc6\xbc\xbdo\xeaQ\xcaO\xae,\xf5\xce3\xddp\x92\x94}\x94_\xac\x97\x1a\x80\x18XD\x13?;\n"\xf7\xd3C\xa6>\x0c2\xf98\x97\xb0\xb9l\xc2z\xc2\xd52\xfa\xac\x85\x9f\x8f\xf7\x06\xa82K\xe1\xb2H\x8b\x97\xefE\x03b\x1f\x97\xbfL\xc6E\x91\xbe4\xeb\x1e9\xef\x8e\x06.\xbc\x92\xce\xbb\x89\x8a\xe7m\xb5\xef\x1b\xaf\x02\xcf\xcf\x80\xf7QH\xb7UA4o2\x93b\x1d\x173\xe1\x01\x8c\xc5\x92\x0f6c5}o.\xc4\xe1\x99\xa1\x1f.I\x0c\xdb\x0f\x01&k\x82\xed\\}\xa5\xadR[anB\x8b\x9d\xd3\xd4+\x00\xb5p\xf9>\xe7\xcc'
        assert client.fake_blinds[1] == b'Jw\x81N\xa6\x14.[\xf7\x8d\x99R\xa3\xeeT\xd4?d\xc5\x0c\xbe\xea\xac\x97\xfc\xd5\x8c\x0f~!\xb8\xaa\x11W\xc8\xb3\xbf\xaf\x9e/\xf7\xad\xc0\xae\xe5\xdd`\x01\xb3\x12\xado\xbb\xdcU\xa2\xf9w\xed\xf4\x95\x9d\x13=\x9f"\xce\n\xdcz\x92\x83V\x04\xc3\xb6g\xbe\x99\x98\xf8fh\xc1m\x05\xc8\x18\x94P\x08[c\xa0)\xa5\xad\xb5UV\x00\xe6\xa3\x05\x86\xb4o\x01\\\x03\x15\x1c2\x86B8\x87\xec\xbe\x86\xab9 4\x9e\xba\x87us\x0b\x19\xec+\x99\x9f\x07\xb3\xf0\xb9LN*\x89\xf5\xfc\xd2m\xad\xfc\xd2\xcf\x1e\xb6N\x17/\xbe\xa0\x1c\xa0\xef\xfev\xe0h\xb1\xf3\xc9\x84T`&\xd5\xa7\xeb.\x99\xd0&\xa7v*+\xa5\xec]\xf2\xc7\xfc\xad8\x882\xe9\xc0i\x82\xceI\xde\xbaw%\xa3\xd4T\xf3m\xbd\x12\x96\xcd\xe1\xb4\xa9`\xb8\xe7\xdf\x9b\x99!I\xe8\xa2\xb2I\xabG\x12/\xaa\xfe\xad;\xed\x00\xfd\xfe\xae\x8e\x90?\xd943\xb6\x0ca\xe4\x06\xa6`\xa7\xa7\xb7'

        #TODO: add check for two of puzzles

        ret = server.solve_puzzles(puzzles)
        assert ret is not None

        ciphertexts, commits = ret
        assert len(ciphertexts) == expected_num_puzzles
        assert len(commits) == expected_num_puzzles

        assert ciphertexts[0] == b'\xbdo\xc5$*\xb8MGB\x97t\xa8\xe3\xde\xef\xfc\xa2\xa8\x81X\xe2,\xea\xa7\xcf\xfe\xa2\xd9vR\x8b}\xb0\xb6{\xa0n\x11x\xb7k\xa9&-\xa09\x00`\xc4/%\xa6\x86\xb7mfcr\x89\xfc\x14\xa3\xb8\xc12\x02\x8bE\xf6\xb5\x93%\xcb\xacq\xf7\x01~\x90\xe0F^nS\x82\xf3\n\x8e\xdbs\x9e\x03\xe9\xce\xa1\xcb\xdfl\x18Q\x9cEL\x07)Y\x8f\xb0\xb6\xc9\x0e\xb3~\xdf\x04kC\xf8cM\xc9\xadN&{d\x17\x1f\x7fYA\xc5\xcf\x94\x17\xfa\x8cHH\xe0\x04\'\xcf\x00\x14\xfd\xdc\xb1\xde\xe1\x8b=\xc9\x1f\xa2\xa8\x8cU\x10\x1e\xdf\xd9f\xc2 Q\x05\x97\x17\x10\xe8\xcc\x86\x89\xd2\xe4\x18TD%N\xb7\xfd\x1e\x9eY\xed7I[pE\xca\xfd\xa6\x10Qe\xeb\xf2\xf7\x11P\xd5\x14\x95F\xf6Ot\xa5\x90\x8f\r\x13\xb9\xbaP\x16\xcd\x85k\x90@o\x1b\x18\xbcSv\xa3V\xaa\xcdW;\x81\x98\x1eq\xc2X-\x88\x88\x10\xfb\xec\x12\x94\x03\x08\xf8\x8b\x7f\xd6\xaeK\x1e\xebuy\x7f"'
        assert ciphertexts[1] == b'o\n\xefO~`J\xc2{\x8f0,:\xb7io\xd67\x8b\r\xf8\x1f>\xdd\x81\x16`n\xb1\x0b0\xa4\x07\xb0rF\xb3\xe7p\xea\x14\xa3\xea\x03g\x80.>\x16O\x10\x96\x0e+n\x15u\xa7\xdaP\x0e^\xf5\xaf7Ap\x8f\x0b\xf5\x865\x90l\x84*\xc7\x14L\xb1\\\xf3\xec\t\xe4\xb2\xb9\xe1\xdd\xd9\xe3\xc9\x8d\x90\xb8p\n\n\x90\xd8\x12a5\xf3\xc8\x1f\x96x\xce\x97J\xcb\xa3i\x03\xd7w\xd3\x84\xdch\x936\x0bB\x06\x1a\x96\xbd\x99QN\xf5"\xe7V|gWcw\xc7\xab\x8a\xf9%\x97\xbav\x0c\xdc\x18pwc\x891\xd9v{\xeas\xce?*\xd7\xc8\xf1Y\xd9\x8a\xa7\xa9\xb4\x9b\x1be\xa6{\xc5Dm\x90T;d\xec\xa2\xd8\xe5k&\x9eB,\xdb\x16\x90P\x80\xcc\xed\nv\xef@\xfaA\xfb\xebv \xa4qS\x8b\xeeG\x86\xa1\xf2\x12\x17\xea\xd7\x82I\x840v)z\xe2\xec\xd0\xb4\xadY\xc6t\xd3\xea[1\xce*(\x90\x84\xff\x1fg\xb8\x80!\xe7\xb8v\x88Z\x7f\x11\x84&'
        assert commits[0] == b'\xc3C2\xb6<\x95?c\x0e\xd0TX\xbd\xac\xea\xbe\xec\x97Z\x11'
        assert commits[1] == b'\x12h\xea\x95\xa2(k\xafp\xb1\xbc\x87\xd1\x95S\xec\xb8\x86\xd8{'

        #TODO: add check for two of ciphertests

        fake_keys = server.verify_fake_set(client.F, client.fake_blinds)
        assert fake_keys is not None

        ret = client.verify_fake_solutions(ciphertexts, commits, fake_keys)
        assert ret is True

        keys = server.verify_real_set(client.puzzle, client.R, client.real_blinds)
        assert keys is not None

        solution = client.extract_solution(ciphertexts, keys)
        assert solution is not None

        assert solution == b'\x82\x814\x97X5\x14, b\xb30 \xe5\xb3`\xbb\x8a\xf6\xce\xb17q[\xa9]\xc9\x01\xf4\x06\x97\x0c4\x93\x15\x00\xf9?Ksdv\x91\xd1\xb4\xd7\xca\x7f\xb1%nJ\xa3\xb5l\x90\xa4,\x9b\xe2c\xc7a\x01\xd0\xdf\x81+\x1b\x9c\xab\x0c~\xae.W|"\xce(\x96\xed\xfc0\xc2\xf4\x00\x02\xe4\xa3|h*{/\x8f\xfb\x8a\xfaz\xfd$\xcc\xa0vK\xe7L\xdafJ@\xf5Y@\xbe\xd0\xeb\xe4\xf2\x0fY\xf0\x03\x8f\xd5\x0e\xb3\xe8\xd1\x9f\x0e*\x90X\x0e\xef:T\x9b\xd1\x11\x1e\x07{\x1c\x88\xdb\x17\x1b\x8f\xa2)~u\xd9\x98k\x03\x16\xdbq\xe29\xd4\xb5\xe0\xc0\x1fXI\xa2\xac\x07&\xa0\xdf\xdc\xd5w\xc7\xec\x96\xd3\xb4\xf1\x0b\xdc\xab\xb3\xbf\x85\x96\xb5\xa3L\xb7\xe02\xf0\x90\xc5\xeb\x07\x8c\x9e\xfcY\xcd_\x140\x9e\xe0\x9eVZt\xcaH\xaf\'\xdb2\xd8\x17s:\xd2\xbd\x91\xbb\xee\x80!G\xcf\xa4\xef\xd1\xb1\x13\xd5\x9d\x840\tM.3\xd0\x8cm;\x10\xb5'
        assert hexlify(solution) == epsilon
