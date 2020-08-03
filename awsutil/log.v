 {
 "files": [
  {
   "fid": 2,
   "path":"/source/demo_benchmark/c_testcase/advance/wp_eg_npd.c"
  },
  {
   "fid": 4,
   "path":"/source/demo_benchmark/c_testcase/advance/wp_eg_obj_sensitive.c"
  },
  {
   "fid": 6,
   "path":"/usr/include/x86_64-linux-gnu/bits/byteswap.h"
  },
  {
   "fid": 7,
   "path":"/source/demo_benchmark/c_testcase/advance/uaf.c"
  },
  {
   "fid": 8,
   "path":"/usr/include/stdlib.h"
  },
  {
   "fid": 9,
   "path":"/source/demo_benchmark/c_testcase/advance/global.h"
  },
  {
   "fid": 10,
   "path":"/usr/include/stdio.h"
  },
  {
   "fid": 11,
   "path":"/usr/include/libio.h"
  },
  {
   "fid": 12,
   "path":"/usr/include/x86_64-linux-gnu/bits/sys_errlist.h"
  },
  {
   "fid": 14,
   "path":"/source/demo_benchmark/c_testcase/advance/uiv.c"
  },
  {
   "fid": 16,
   "path":"/source/demo_benchmark/c_testcase/advance/aob.c"
  },
  {
   "fid": 18,
   "path":"/source/demo_benchmark/c_testcase/advance/asm_uiv_npd.c"
  },
  {
   "fid": 20,
   "path":"/source/demo_benchmark/c_testcase/advance/msf.c"
  },
  {
   "fid": 22,
   "path":"/source/demo_benchmark/c_testcase/advance/xplatform_32_64.c"
  },
  {
   "fid": 24,
   "path":"/source/demo_benchmark/c_testcase/advance/wp_eg_npd_ctx.c"
  },
  {
   "fid": 26,
   "path":"/source/demo_benchmark/c_testcase/advance/main.c"
  },
  {
   "fid": 28,
   "path":"/source/demo_benchmark/c_testcase/advance/npd.c"
  },
  {
   "fid": 30,
   "path":"/source/demo_benchmark/c_testcase/advance/dbf.c"
  },
  {
   "fid": 32,
   "path":"/source/demo_benchmark/c_testcase/advance/global.c"
  }
 ],
 "issues": [
  {
   "fid": 26,
   "sln": 12,
   "scn": 0,
   "k":"memmodel_clang1@FAM@main.c:12@wp_eg_obj_sensitive.c:6",
   "rs":"BUILTIN",
   "rc":"FAM",
   "ec":null,
   "c":"D",
   "ic": 6,
   "vn":"memmodel_clang1",
   "fn":"main()",
   "m":"${FAM.1}",
   "paths": [
    {
     "fid": 4,
     "sln": 6,
     "scn": 0,
     "m":"${path.msg.4}",
     "vn":"memmodel_clang1",
     "fn":"memmodel_clang1()"
    },
    {
     "fid": 26,
     "sln": 12,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":null,
     "fn":"main()"
    }
   ]
  },
  {
   "fid": 2,
   "sln": 6,
   "scn": 0,
   "k":"p@NPD@wp_eg_npd.c:3",
   "rs":"BUILTIN",
   "rc":"NPD",
   "ec":null,
   "c":"D",
   "ic": 18,
   "vn":"p",
   "fn":"npd_simple()",
   "m":"${NPD.1}",
   "paths": [
    {
     "fid": 2,
     "sln": 3,
     "scn": 0,
     "m":"${path.msg.27}",
     "vn":null,
     "fn":"npd_simple()"
    },
    {
     "fid": 2,
     "sln": 5,
     "scn": 0,
     "m":"${path.msg.27}",
     "vn":null,
     "fn":"npd_simple()"
    },
    {
     "fid": 2,
     "sln": 6,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"p",
     "fn":"npd_simple()"
    }
   ]
  },
  {
   "fid": 2,
   "sln": 24,
   "scn": 0,
   "k":"q@NPD@wp_eg_npd.c:14",
   "rs":"BUILTIN",
   "rc":"NPD",
   "ec":null,
   "c":"M",
   "ic": 27,
   "vn":"q",
   "fn":"npd_complex()",
   "m":"${NPD.1}",
   "paths": [
    {
     "fid": 2,
     "sln": 14,
     "scn": 0,
     "m":"${path.msg.1}",
     "vn":"q",
     "fn":"npd_complex()"
    },
    {
     "fid": 2,
     "sln": 17,
     "scn": 0,
     "m":"${path.msg.17}",
     "vn":null,
     "fn":"npd_complex()"
    },
    {
     "fid": 2,
     "sln": 18,
     "scn": 0,
     "m":"${path.msg.17}",
     "vn":null,
     "fn":"npd_complex()"
    },
    {
     "fid": 2,
     "sln": 24,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"q",
     "fn":"npd_complex()"
    }
   ]
  },
  {
   "fid": 2,
   "sln": 46,
   "scn": 0,
   "k":"q@NPD@wp_eg_npd.c:30",
   "rs":"BUILTIN",
   "rc":"NPD",
   "ec":null,
   "c":"M",
   "ic": 27,
   "vn":"q",
   "fn":"npd_cross_func()",
   "m":"${NPD.1}",
   "paths": [
    {
     "fid": 2,
     "sln": 30,
     "scn": 0,
     "m":"${path.msg.1}",
     "vn":"q",
     "fn":"another_func1()"
    },
    {
     "fid": 2,
     "sln": 33,
     "scn": 0,
     "m":"${path.msg.17}",
     "vn":null,
     "fn":"another_func1()"
    },
    {
     "fid": 2,
     "sln": 34,
     "scn": 0,
     "m":"${path.msg.17}",
     "vn":null,
     "fn":"another_func1()"
    },
    {
     "fid": 2,
     "sln": 45,
     "scn": 0,
     "m":"${path.msg.18}",
     "vn":null,
     "fn":"npd_cross_func()"
    },
    {
     "fid": 2,
     "sln": 46,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"q",
     "fn":"npd_cross_func()"
    }
   ]
  },
  {
   "fid": 18,
   "sln": 6,
   "scn": 0,
   "k":"b@UIV@asm_uiv_npd.c:4",
   "rs":"BUILTIN",
   "rc":"UIV",
   "ec":null,
   "c":"D",
   "ic": 5,
   "vn":"b",
   "fn":"asm_add()",
   "m":"${UIV.1}",
   "paths": [
    {
     "fid": 18,
     "sln": 4,
     "scn": 0,
     "m":"${path.msg.4}",
     "vn":"b",
     "fn":"asm_add()"
    },
    {
     "fid": 18,
     "sln": 6,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"b",
     "fn":"asm_add()"
    }
   ]
  },
  {
   "fid": 22,
   "sln": 11,
   "scn": 0,
   "k":"SIZE:8@MEM35-C@CERT@xplatform_32_64.c:11",
   "rs":"CERT",
   "rc":"MEM35-C",
   "ec":null,
   "c":"D",
   "ic": 20,
   "vn":"SIZE:8",
   "fn":"xplatform_test()",
   "m":"${MEM35-C.1}",
   "paths": [
    {
     "fid": 22,
     "sln": 11,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"SIZE:8",
     "fn":"xplatform_test()"
    }
   ]
  },
  {
   "fid": 22,
   "sln": 18,
   "scn": 0,
   "k":"a@AOB@xplatform_32_64.c:18@xplatform_32_64.c:11",
   "rs":"BUILTIN",
   "rc":"AOB",
   "ec":null,
   "c":"D",
   "ic": 40,
   "vn":"a",
   "fn":"xplatform_test()",
   "m":"${AOB.1}",
   "paths": [
    {
     "fid": 22,
     "sln": 11,
     "scn": 0,
     "m":"${path.msg.5}",
     "vn":null,
     "fn":"xplatform_test()"
    },
    {
     "fid": 22,
     "sln": 12,
     "scn": 0,
     "m":"${path.msg.24}",
     "vn":null,
     "fn":"xplatform_test()"
    },
    {
     "fid": 22,
     "sln": 12,
     "scn": 0,
     "m":"${path.msg.26}",
     "vn":null,
     "fn":"xplatform_test()"
    },
    {
     "fid": 22,
     "sln": 11,
     "scn": 0,
     "m":"${path.msg.27}",
     "vn":null,
     "fn":"xplatform_test()"
    },
    {
     "fid": 22,
     "sln": 18,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"a",
     "fn":"xplatform_test()"
    }
   ]
  },
  {
   "fid": 24,
   "sln": 31,
   "scn": 0,
   "k":"p@NPD@wp_eg_npd_ctx.c:7",
   "rs":"BUILTIN",
   "rc":"NPD",
   "ec":null,
   "c":"M",
   "ic": 36,
   "vn":"p",
   "fn":"npd_cross_func_ctx()",
   "m":"${NPD.1}",
   "paths": [
    {
     "fid": 24,
     "sln": 7,
     "scn": 0,
     "m":"${path.msg.1}",
     "vn":"q",
     "fn":"another_func()"
    },
    {
     "fid": 24,
     "sln": 10,
     "scn": 0,
     "m":"${path.msg.17}",
     "vn":null,
     "fn":"another_func()"
    },
    {
     "fid": 24,
     "sln": 11,
     "scn": 0,
     "m":"${path.msg.17}",
     "vn":null,
     "fn":"another_func()"
    },
    {
     "fid": 24,
     "sln": 23,
     "scn": 0,
     "m":"${path.msg.18}",
     "vn":null,
     "fn":"npd_cross_func_ctx()"
    },
    {
     "fid": 24,
     "sln": 23,
     "scn": 0,
     "m":"${path.msg.1}",
     "vn":"p",
     "fn":"npd_cross_func_ctx()"
    },
    {
     "fid": 24,
     "sln": 23,
     "scn": 0,
     "m":"${path.msg.17}",
     "vn":null,
     "fn":"npd_cross_func_ctx()"
    },
    {
     "fid": 24,
     "sln": 31,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"p",
     "fn":"npd_cross_func_ctx()"
    }
   ]
  },
  {
   "fid": 32,
   "sln": 7,
   "scn": 0,
   "k":"a@AOB@global.c:7@aob.c:6",
   "rs":"BUILTIN",
   "rc":"AOB",
   "ec":null,
   "c":"D",
   "ic": 35,
   "vn":"a",
   "fn":"aob_assign()",
   "m":"${AOB.1}",
   "paths": [
    {
     "fid": 16,
     "sln": 6,
     "scn": 0,
     "m":"${path.msg.2}",
     "vn":null,
     "fn":"test_aob()"
    },
    {
     "fid": 32,
     "sln": 6,
     "scn": 0,
     "m":"${path.msg.4}",
     "vn":"a",
     "fn":"aob_assign()"
    },
    {
     "fid": 32,
     "sln": 7,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"a",
     "fn":"aob_assign()"
    }
   ]
  },
  {
   "fid": 32,
   "sln": 21,
   "scn": 0,
   "k":"p@DBF@global.c:21@dbf.c:7",
   "rs":"BUILTIN",
   "rc":"DBF",
   "ec":null,
   "c":"M",
   "ic": 42,
   "vn":"p",
   "fn":"dbf_free_2()",
   "m":"${DBF.1}",
   "paths": [
    {
     "fid": 30,
     "sln": 7,
     "scn": 0,
     "m":"${path.msg.9}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 30,
     "sln": 8,
     "scn": 0,
     "m":"${path.msg.24}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 30,
     "sln": 8,
     "scn": 0,
     "m":"${path.msg.26}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 30,
     "sln": 13,
     "scn": 0,
     "m":"${path.msg.10}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 30,
     "sln": 14,
     "scn": 0,
     "m":"${path.msg.2}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 32,
     "sln": 19,
     "scn": 0,
     "m":"${path.msg.15}",
     "vn":null,
     "fn":"dbf_free_2()"
    },
    {
     "fid": 32,
     "sln": 19,
     "scn": 0,
     "m":"${path.msg.1}",
     "vn":"p",
     "fn":"dbf_free_2()"
    },
    {
     "fid": 32,
     "sln": 20,
     "scn": 0,
     "m":"${path.msg.23}",
     "vn":null,
     "fn":"dbf_free_2()"
    },
    {
     "fid": 32,
     "sln": 21,
     "scn": 0,
     "m":"${path.msg.25}",
     "vn":null,
     "fn":"dbf_free_2()"
    },
    {
     "fid": 32,
     "sln": 21,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":null,
     "fn":"dbf_free_2()"
    }
   ]
  },
  {
   "fid": 30,
   "sln": 14,
   "scn": 0,
   "k":"p@DBF@dbf.c:7",
   "rs":"BUILTIN",
   "rc":"DBF",
   "ec":null,
   "c":"M",
   "ic": 24,
   "vn":"p",
   "fn":"test_dbf()",
   "m":"${DBF.1}",
   "paths": [
    {
     "fid": 30,
     "sln": 7,
     "scn": 0,
     "m":"${path.msg.9}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 30,
     "sln": 8,
     "scn": 0,
     "m":"${path.msg.24}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 30,
     "sln": 8,
     "scn": 0,
     "m":"${path.msg.26}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 30,
     "sln": 13,
     "scn": 0,
     "m":"${path.msg.10}",
     "vn":null,
     "fn":"test_dbf()"
    },
    {
     "fid": 30,
     "sln": 14,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":null,
     "fn":"test_dbf()"
    }
   ]
  },
  {
   "fid": 20,
   "sln": 19,
   "scn": 0,
   "k":"p@MSF@msf.c:8",
   "rs":"BUILTIN",
   "rc":"MSF",
   "ec":null,
   "c":"D",
   "ic": 18,
   "vn":"p",
   "fn":"test_msf()",
   "m":"${MSF.1}",
   "paths": [
    {
     "fid": 20,
     "sln": 8,
     "scn": 0,
     "m":"${path.msg.9}",
     "vn":null,
     "fn":"test_msf()"
    },
    {
     "fid": 20,
     "sln": 17,
     "scn": 0,
     "m":"${path.msg.12}",
     "vn":null,
     "fn":"test_msf()"
    },
    {
     "fid": 20,
     "sln": 19,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":null,
     "fn":"test_msf()"
    }
   ]
  },
  {
   "fid": 32,
   "sln": 35,
   "scn": 0,
   "k":"a@NPD@npd.c:5",
   "rs":"BUILTIN",
   "rc":"NPD",
   "ec":null,
   "c":"D",
   "ic": 24,
   "vn":"a",
   "fn":"npd_assign()",
   "m":"${NPD.1}",
   "paths": [
    {
     "fid": 28,
     "sln": 6,
     "scn": 0,
     "m":"${path.msg.2}",
     "vn":null,
     "fn":"test_npd()"
    },
    {
     "fid": 32,
     "sln": 34,
     "scn": 0,
     "m":"${path.msg.4}",
     "vn":"a",
     "fn":"npd_assign()"
    },
    {
     "fid": 32,
     "sln": 34,
     "scn": 0,
     "m":"${path.msg.1}",
     "vn":"a",
     "fn":"npd_assign()"
    },
    {
     "fid": 32,
     "sln": 35,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"a",
     "fn":"npd_assign()"
    }
   ]
  },
  {
   "fid": 7,
   "sln": 16,
   "scn": 0,
   "k":"q@UAF@uaf.c:7",
   "rs":"BUILTIN",
   "rc":"UAF",
   "ec":null,
   "c":"M",
   "ic": 21,
   "vn":"q",
   "fn":"test_uaf()",
   "m":"${UAF.1}",
   "paths": [
    {
     "fid": 7,
     "sln": 13,
     "scn": 0,
     "m":"${path.msg.10}",
     "vn":null,
     "fn":"test_uaf()"
    },
    {
     "fid": 7,
     "sln": 7,
     "scn": 0,
     "m":"${path.msg.27}",
     "vn":null,
     "fn":"test_uaf()"
    },
    {
     "fid": 7,
     "sln": 12,
     "scn": 0,
     "m":"${path.msg.27}",
     "vn":null,
     "fn":"test_uaf()"
    },
    {
     "fid": 7,
     "sln": 16,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":"j",
     "fn":"test_uaf()"
    }
   ]
  },
  {
   "fid": 32,
   "sln": 49,
   "scn": 0,
   "k":"a@UIV@global.c:49@uiv.c:6",
   "rs":"BUILTIN",
   "rc":"UIV",
   "ec":null,
   "c":"D",
   "ic": 6,
   "vn":"a",
   "fn":"uiv_assign()",
   "m":"${UIV.1}",
   "paths": [
    {
     "fid": 14,
     "sln": 6,
     "scn": 0,
     "m":"${path.msg.2}",
     "vn":null,
     "fn":"test_uiv()"
    },
    {
     "fid": 32,
     "sln": 49,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":null,
     "fn":"uiv_assign()"
    }
   ]
  },
  {
   "fid": 18,
   "sln": 12,
   "scn": 0,
   "k":"p@NPD@asm_uiv_npd.c:10",
   "rs":"BUILTIN",
   "rc":"NPD",
   "ec":null,
   "c":"D",
   "ic": 15,
   "vn":"p",
   "fn":"asm_deref()",
   "m":"${NPD.1}",
   "paths": [
    {
     "fid": 18,
     "sln": 10,
     "scn": 0,
     "m":"${path.msg.1}",
     "vn":"p",
     "fn":"asm_deref()"
    },
    {
     "fid": 18,
     "sln": 12,
     "scn": 0,
     "m":"${path.msg.3}",
     "vn":null,
     "fn":"asm_deref()"
    }
   ]
  }
 ],
 "rulesets": [
  {
   "rs":"BUILTIN",
   "rv":"1"
  },
  {
   "rs":"CERT",
   "rv":"1"
  }
 ],
 "v": 1,
 "id":"6ecdaa8f-302d-4d93-b84d-c5ff9f4123e5",
 "s":"@@status@@",
 "m":"@@message@@",
 "eng":"Xcalibyte",
 "ev":"1",
 "er":"e47bf8ace9daea06255733e7a170870b083b83c1(develop)",
 "x1":"yv#@hk#@EHZ*qhlm.8#@EHZ*nhtrw.8#@GZIT*zyr.m35#@GZIT*kilxvhhli.xliv#@EHZ*zfgsvm.8#@EHZ*glpvm.vbQsyTxrLrQRFaFcNrQ#@EHZ*hvievi.807~831~9~870@19#@EHZ*xvigx.8#@EHZ*avil_tolyzo.9#cehz@cuz@wfnnb~x",
 "x2":"SLNV./illg,SLHGMZNV.06wuxxx390v2,OW_ORYIZIB_KZGS./dh/cxzo/zkk/cehz/yrm/~~/r313@kx@ormfc@tmf/c13_35@ormfc/ory*/dh/cxzo/zkk/cehz/ory/8~9,KZGS./fhi/olxzo/hyrm*/fhi/olxzo/yrm*/fhi/hyrm*/fhi/yrm*/hyrm*/yrm*/dh/cxzo/zkk/cehz/yrm*/slnv/cxzorybgv/cehz/yrm,KDW./hsziv/hxzm/3vxwzz1u@697w@5w06@y15w@x4uu0u5876v4/hxzm_ivhfog,",
 "ss": 1595261479087130,
 "se": 1595261610553483,
 "usr": 132000,
 "sys": 40000,
 "rss": 55664
 }