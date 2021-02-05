
from random import randrange

uint64_t = lambda x : f'{"0"*(64-len(f"{x:8b}"))}{x:08b}'
uint8_t  = lambda x : int(uint64_t(x)[-8:],2)


def __builtin_clzll(x):
    x = uint64_t(x)
    i = 0
    while(i < len(x)):
        if (x[i] == '0'):
            i += 1
        else:
            break
    return i

# __INTRIN_INLINE bool bsr64(unsigned long* const index, const uint64_t mask)
#     {
# if (mask != 0U) {
#             *index = (unsigned long)(63 - __builtin_clzll(mask));
#             return true;
#         }
#         return false;

def bsr64(mask):
    return 63 - __builtin_clzll(mask)

# inline uint8_t msb(uint64_t x, unsigned long& ret)
#     {
#         return static_cast<uint8_t>(intrinsics::bsr64(&ret, x));
#     }

def msb2(x):
    return bsr64(x)

# inline uint8_t msb(uint64_t x)
# {
#     assert(x);
#     unsigned long ret = -1U;
#     msb(x, ret);
#     return (uint8_t)ret;
# }

def msb(x): 
    assert(x) # uint64_t
    ret = -1
    if (x != 0):
        ret = msb2(x)
    print(f"msb2(x)={ret} uint8_t(x)={uint8_t(ret)}")
    return uint8_t(ret) # uint8_t int('101000000000', 2)


# inline uint64_t ceil_log2(const uint64_t x) {
#     assert(x > 0);
#     return (x > 1) ? pisa::broadword::msb(x - 1) + 1 : 0;
# }

def ceil_log2(x):
    assert(x > 0)
    return msb(x - 1) + 1 if (x > 1) else 0

def ceil_div(dividend, divisor):
    d = int(dividend)
    div = int(divisor)
    return (d + div - 1) // div

header = 2

def posting_cost(x, base):
    try:
        if (x == 0 or x - base == 0):
            return 8 + header # 8 bits value + 2 bit header
        
        assert(x >= base)
        return (8 + header) * ceil_div(
                    ceil_log2(x - base + 1),  # delta gap
                    8)
    except (AttributeError, TypeError):
        raise AssertionError('Input variables should be integers')


def bitsize(x):
    base = 0
    n = []
    cost = 0
    for i in x:
        c = posting_cost(i, base)
        cost += c
        n.append(i - base)
        print(f"\ti:{base}\tbase:{base}\t\ti-base:{i-base}\tcost:{c}\ttotal_cost:{cost}")
        base = i
    return n, cost

docs = [ i for j in range(0, 10) for i in range(j*1000, j*1000+1000, randrange(256, 1000))]
docs_dgaps = bitsize(docs)

# import pdb; pdb.set_trace()

