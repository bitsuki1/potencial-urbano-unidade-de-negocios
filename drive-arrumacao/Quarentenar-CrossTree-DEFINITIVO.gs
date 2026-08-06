/**
 * ============================================================================
 *  QUARENTENAR DUPLICATAS CROSS-TREE — DEFINITIVO (SEM SIMULAÇÃO)
 *  Pedido do dono 2026-08-06: "me traga o script definitivo, sem teste".
 *  EXECUTA DIRETO: move as 198 cópias byte-idênticas para a quarentena datada
 *  em "98 — _LEGADO/_quarentena-cross-DEFINITIVO". NADA vai para a lixeira;
 *  a canônica oficial FICA onde está. IDEMPOTENTE: se você rodar duas vezes,
 *  a segunda não faz nada (arquivo já na quarentena = pulado).
 *  COMO RODAR (uma vez): script.google.com > Novo projeto > colar > executar
 *  a função quarentenarCrossTreeDefinitivo > autorizar > conferir o Log.
 * ============================================================================
 */
var PROJETO_RAIZ_ID = '1BrM6q36meTtn5guJoiGbqvCtZF11Uau3'; // pasta "POTENCIAL URBANO"
var QUARENTENA_RAIZ_NOME = '98 — _LEGADO';
var QUARENTENA_NOME = '_quarentena-cross-DEFINITIVO';

// [dup_id, canonico_id] — do inventario/cross-tree-dups.csv (198 duplicatas)
var DUPS = [
  ['1F__Xn0_m3May46FpP3e6YFNloTdqdfwh', '13AUlueEv40Suw08chbfTIdn6B6-lCCNI'],
  ['1vJxueY0EQljJXYbFmYEVUwfIfJUvjSgc', '1Iz1CZfIfwPWncIyRSW6vHXNIx6VP9gHq'],
  ['1lixqSHNwb-fKnHWkst1upJfr2KbeqpIx', '1wttjXQGDl4I4HuQrxHAinRu_PMgzvuWw'],
  ['1rt_LEy7INQmohKFvcTpfmqZPE9bfbHnz', '1qDGqUnJ4wQYmEMrpWLqPzY0so8qiilB4'],
  ['1bnw3318xqRO870YRmk_y9ZLTC0alyojz', '1yNTpkrckg7JjwwhSku5R-syW0bUKlCOH'],
  ['13y1InqQDm4sabuFFdm-X2WYKyXmM5ekE', '1yNTpkrckg7JjwwhSku5R-syW0bUKlCOH'],
  ['1I8hJa-p6LejAxMdzcS3zwuekaX5g1VLW', '1sxwpkwv9Zyjm8mVKzdTwzEoF3eBdgZgB'],
  ['1K53ehPuflJIUqPrGLRq9vdFyKk_YGJeP', '1sxwpkwv9Zyjm8mVKzdTwzEoF3eBdgZgB'],
  ['185aNsrl-imv65InLqilRtVSKjm3MCJkQ', '1CabM7_WkIMQpAOQY8vp9cctE5KCRTyOC'],
  ['12yID6_KDzJ4N83B0pCXjOWC8KSHy7T0F', '1CabM7_WkIMQpAOQY8vp9cctE5KCRTyOC'],
  ['1594U0HVb7XEmvA4TIO9-qShC6kqlxayS', '1kR1qbgvn8xi5gDSXcy69FTdSvNIaBUSp'],
  ['1XNoWqGwVQywCT73FxPBAjZNLX8TgL2o9', '1kR1qbgvn8xi5gDSXcy69FTdSvNIaBUSp'],
  ['11IbxLz-nUiol2qhZbXPbF4C-_Dwvl4Y4', '1PbLdXi4Yg1jZIHJ0R_rtK99IxoyotI0k'],
  ['1lJcApFuMJM1m8Dxhe9qc4lVdo25qcVVi', '1PbLdXi4Yg1jZIHJ0R_rtK99IxoyotI0k'],
  ['11ZDVwqRPxVk6yPLFCM0GYib1ubLW2587', '1DyRduyd8wLTGtrVdJRH_B3hW5RVxGPuv'],
  ['1vfi39m0QNpBV7NxboRGChtHhAUM-ymVI', '1DyRduyd8wLTGtrVdJRH_B3hW5RVxGPuv'],
  ['1GD9PH2cL9wIm1bMUgjlymQCpHYUdBkS3', '1UUH5feKumfLjaRHNVXuuJ5iWSu98omRH'],
  ['13pyQ0xKDyphWlSJCBBhktxAlCGssjdIb', '1UUH5feKumfLjaRHNVXuuJ5iWSu98omRH'],
  ['1zJXKwtR3mTjuzR06CW78FYO9kod4i4lt', '18DHBwgqGrAaxsj9l09x5nuqFl6gvpZwH'],
  ['1bEBJrLDRgnNcR-lGkBq23n1eF1-XNBLM', '18DHBwgqGrAaxsj9l09x5nuqFl6gvpZwH'],
  ['14Nq6I2YlHrQbUtmTTG2QHDKp7gdeBtvN', '1I6msIG4xWfhKgJFSG2VMp5kU2p1Ms770'],
  ['1y-DTBpeX6qHq4cfLbS822pRhLNYWQUMz', '1I6msIG4xWfhKgJFSG2VMp5kU2p1Ms770'],
  ['1D28Od_TpjJa31RJb9kyHYlPb2ULyytXC', '1jojd4A3qvF0qSnw1KBZ318mt8csLjNc6'],
  ['1kTZFvh7M57bN8aCavgEYTKPJQy0xOwqa', '1jojd4A3qvF0qSnw1KBZ318mt8csLjNc6'],
  ['1B4qqNtC1R6hUjgj1Ilc-Xhbp_FM145Lz', '1L16ZacFYfv4_ABclZe64zOj761m_PK9d'],
  ['1c9sDXAUsHHWjd-Z01vVmmKyHDl5zxqqf', '1L16ZacFYfv4_ABclZe64zOj761m_PK9d'],
  ['1LqHz7kHG-SyqEh4R795mQoQXBUL1FDoH', '1L16ZacFYfv4_ABclZe64zOj761m_PK9d'],
  ['1jWoePqwVaOvpPsHb5PdFDgQ3SNr-4209', '1L16ZacFYfv4_ABclZe64zOj761m_PK9d'],
  ['1FMH9asZA-sGC2Wkr0aORvGRhvAXRJ_0C', '1L16ZacFYfv4_ABclZe64zOj761m_PK9d'],
  ['1GRu3oAkqrUgbKnARw94xmLXcPN6S8Mm8', '1DjNzdv9DhebFkZ8rB6vSWDeuBJUJTIyk'],
  ['17gTnZrKAXVrxRQA0wFHVmqcwBTwii6_J', '1Y467rZEJ4XMTCVWHp6vGYLhiHTshh2cC'],
  ['1JUK_uiInZdrdMNDKpXHA-h4GA2T8c_dv', '19QtvSOOJI1cwjalzNx4PghcPbJ4tbBWu'],
  ['1THtgVEq2HHNNJ5LBUoAFOTfX2Zw96TdO', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1v_eb9tyrOHk0qsBFQjGk_gPrJ9rzqkr5', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1j22wt6DYvqB9t6khrdIz2-PzB6sN4usK', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1r8kXPeBpzs4rmJE7JoeF2qm-aAxlO9PH', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1PuO2wyKZeXyEvibtdkRE4vn5RuejWstS', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1I0Zden8s7K8WyZxPaQ4ZoueYKqKi-T5L', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1GwE10ccA5XPcJ4KWbRFyIMaC6F1wI_qc', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['17EK318mHaIqnV6zngNqsKWfHLsG7mOus', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1KpeyXXyOwk1itnRe2VLZqtjKPqU43i0M', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['11X9pA3X7B37e4Kz6mjpfjGi7FxsIlD8e', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1E-U2w2uuBUOUWrP_gQahCKJAKbo7MIY1', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1-1l5WX_B4kJaTZZqs71Mc0Vrfq5_1TB6', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1NNgCwbalBxqbiajwAxASzPDjA2n_KNeB', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1UmiZxDGYHBXoVUMwu0fh5FvorFHZU0ZZ', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['11ENoXVqE2vwLPnRV5WthJK9Acz6mXqMg', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1XoLIjyMLOe6RjBnyp0_Hn6z0ukrc1he4', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1BeLw8VxIGtdKgbM5vK2CrJZJPaQMwO_S', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1k7dWQnUiDP4SA-2b0cqaZH1xn_2lMZyz', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1bvTWNnM0i10uPcmzLmaVBYSIEjvar4n4', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1zTbM-1npNoCt5xx-UQ4gscJRr2z4EtwN', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1FqzSYgJSvxMaF2U7GmmvrjZVdtA8eAFo', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1AHFkXkEcOm7ZXherKPNzZNirVrtRBPdF', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1z6_rUUaLWE2y26u3L7AfL06hGS4S2vz0', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['101IZhOOzGu8yWoaA273eFAL4FEsF9xgp', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1j7SXNgKGF6SV_K4g1gC7bQe8yu-az92s', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1cnUxpN8PQtfUr7_f1QWIn0Bh0xe88V-y', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1D2gCtB7tgktMkArnCdndXCvo3ey2xtD-', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1CsTqoHKAxTXvunxlNxNBAd0OfaF0Zb4K', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1TT01AglMypnG_uIIYyT3wmoYpgy4Wj6K', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1VNTq2wFxsdMr_1UTV3wlS9mBAvudqsR0', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1t_V0JXd2obS3LQn0JtF91lEZM4-9xW7d', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1bukkA1yC1uvgpuE06XIy80ooSrLL7rDh', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1xIPee6JRr_FcCMIHKyzdp-s9n4Vwdn4T', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1tNyKu7_jvBiGuJVnjbPcuTb_OQ4RNqkw', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1WH8pm-8Rll-gENuAvCcAqb_FV5loPAio', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1faC3uBUqtf1NGdx0wvm7jhCsa98WdKqq', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1lY-iv2Ds6ycpG5DCAR3QK5evnIG6C-hv', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['142Txax4yH5Y_Vx7p7K6T0u9G1ctlqGKt', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1cfOnZ3qmpDmjuQhquQLitUT85NDzQ4F-', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1tbVJvIZdPBinruXVRnH5S7R2OAcWPSiE', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1QCD4RbojOSV1KY9DARFdh1u9_ZspBm6Z', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1DqVy_YrIJ-MaK_NH8X8r5Ts8m1d3AHPN', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1xvidK_pYLxL0zcsdc__qVq-YCccIe7HL', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1KPANSI-3vrOPbmLDVpavFUJAF4p-NwtV', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1qvP6opEpfvWLZQbG-VdGk5gAZJJf7F6v', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1pZ5TWPULUVU6JfRBpaeKeOpqznCX2jtN', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['18bkQFmS6oCGjcVR99iAsrFISW437pARe', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1uGXS16lLvzlgJWpdyLcfG4HfZxR5Eig-', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1hNEsLDeCM1JMUfmlefQhbzhVE4od2q4X', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1cZa2f_HZWH0Dj2dFIPuE_YZPW0H1Ay96', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1fJy9aEeNfI9ZK0OkRCmzCWWbGMABnCl1', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['11rN6AzOLinEiBNtbnAkrG4_yUGWBdDQe', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['12JSu0C2my6N0GOBVu75CL6pSLEN6nx5z', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['11xPsitBpfR5X2EBPoMDNLtRLg1jGP0RF', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1tEllev86gObzqgBhlNCso5WYmuBrNUVj', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1X0L95B2_c8GZZpSO28ZJr9gzuRlufXF_', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1-K3FtacDgTlOaCOQQHW3oAE4-Y0JfAIs', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1AM84aI9StYAUwr_dN6N8KE7s4TthyJh4', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['11eEW2g3134uAOATczvtTFbJ7m6VUAiEy', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1Zj211JgFH34wPQ7pxTjeBp8JLbGGA67n', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1zIXf9BOp89YmIGMoCKq9nIWOXtIIH5oW', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1ReRixQGo-bPkjsCN1Wo8vfS1KWisO6px', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1MwFCWES_0ddcrcb9MU8mBgkJT0DvhVy4', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1PDVAGQPFStfb6PEtgt5ICSMMoEvtgFdG', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1E5g6kteH1lGlB8oIgAOaThG9lzc6WHpc', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1FRyPpyw_jSpgSbLkrACxkK4-MCOpGdZY', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1s48BP8AfvaERKUaGcgYDxqfO-_FaxtpA', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1xhXWWWQfKPSXqkYvY1CwvEIxwmidNQLy', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['14r7NA6qBsKhy8APnbYc-r_EMCFYHnzFc', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1sdWEODP2kMw5AZHz86P9hckBysiL7i-j', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1mIDoDCxn3u7W9ZbJNyMzTy--O4a-2VId', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['10_10_m0aRqTpEZOYYvL8cQTgCmCCshJY', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1VWDMVbDrotmUnB-_RQylKKfP6ARV5bQQ', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['17jewm5IpeGMr6n1nECWvbioGvLHPXZ8r', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1iDZ1_gWp191s1gPkmWRnds7RtnI6fF-8', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['19PYoUsNmsppLIBJwJByxX96IQyFhC3m0', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1OKxXmh5-uGKDII3McafwcwV3C4VMmm74', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1GM0ZzZHxZ93vcwA5ygcnP4oke-l0k1cI', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['10EZsQiR9Bhau-MOAZpMN_1yxqVct403c', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1yOPzCx8m-aMSRGHL31QfVSBHB88d1HLN', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1-at5Mmz0ztlQxyqOrgzyalEVmVgfp4qB', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1e5oIvaoDKn0SibfCHEpSE1kgfJcc-4am', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1TdKA4mDT4H976x7hQlF7uJZsO7H-U9Es', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['18hA6uejfmAZsthA26Udjy5jrVrt3NE52', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['19qYE-rX43kA7ZGapJthIxSiydChkcjsK', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['17enXtYVOLdxaWSr7icsS7m3E9CUZhTVP', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1P-gY6SB1Cm43cz5v3-52lKoQGpTeubvn', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1L7Rphc5FU53qnf2-Pqx6dC5k9uEPbHMz', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1n74XdX1nxnbT_Fyi83NtVfSdfxtBF0G9', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['17KR6W7hhqS3nUD79baMxO6f0MjxUfTEi', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['12Q9SmPl-Qe6NiNLxqdJwhBhpPyeDknsf', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1uAyLNmKuUkwL_QWlFuKZs_xRh-Z54qxe', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1bsGK2oOnRfqPrbuu3DedqBm8PyrR-vks', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1-G-UzkDH6Cc-4EeSu700M33QJkJG7VKW', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['128wh5SFO5Orem2Y-j0chcdi34OpJGB1j', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1syilzKHETZGALQaYLP-D9_3sX0t2tyHB', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1H4w4tUFOHCbqf66cRJv5bn1eKDm4Lr9K', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1nsa2UCrz1ovHQHF7duVXpOPnOFJ568jX', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1579ulMrrS-11MTa09SDDv25cfqmMbtxP', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1SdJDrkMzbdD9G_f7Qj1OlF74CdZ_laoe', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1Wyb4iCOpmRo-xiHaVCEFNe33GcN3PxGa', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1ZWyhj0yMoy9GMWyLXPZnE6CmWm3ex_Y9', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1qmEc9-zX8i4w2h_ZsytCuOxgXSLQoFJO', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1BMgJcQWuHsMm8HhBslvar17cZv7bcgP2', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1ngyMLmE4bWP-cD-qxct9MiI2RcW_amLz', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1SFqEyhLRYOP4szYfkIGNgIZk3HK_6MZc', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['15E66KeFoFh8D0xuTreq1AvxDovbYE65B', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['12B7OLTZY3K6NChQ3FYMHjEpqgHXm0USZ', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1Hxg3YrdhTZbMKZ_xujoLkQA9Ph1f7D9l', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1h4iZi96LST8biJ2Stwz8BWJYY5Fu6uig', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1ag9iPMY-o3pV7NnSwcCH1xj4K1Bg8VQD', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1GT6XFSFC_5kRhBKyYgO_HC_PTP7zJql1', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1TysWMS_9E3d1U-wSNpmqloUUmhRSknMA', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1tb7C_wDN0gUmpKsfB6bycOwin57rVwqM', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1Sll7KE-QKAH5f-UM2xRJ6aaKn0yvmPTl', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1nKmp9gFN9Tc3oM0xlVUfYGkXDwDznHrw', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1U8dsyHRzUMo1lsrcG89pG0FL7aE6Y2Cn', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1iVhM8LnKSoZwuiV1MXTfrGad_mq5x6kY', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1mmK_Gkh-sYrPz3jYqyMzmmxfYptr7ZMe', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1VIJzUsxJ4elh9ypdyShA0n0ADmK7IfJA', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1vMGIHNL1kd2TLXoaGLqcu8pOgXlh-xZF', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1YkR0bWqMFnVLvXaeewKPuuoo9r0_y4nJ', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1G1_bQdeVaUvzSfard_wW6uBJmZy5TUj8', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1xI4KkfhBV8Vu_3dhAcja3S8ITh09XbWr', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1LV_0IPE3-GttNX1bbotmbl1lDNxvGPDT', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1XuYeON374NXQ_0g8PBYT8Wz09eLbJF5E', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['15kVJEMEjfSf20xHi2b-dvCwHN5bzaLrt', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1J7SBx8hBFwZEga840Yq0PSsPzWwEvqFG', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['190EZ5kAGnHsiHMNyIYcxLhP_aeC9nztc', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1FPAlI-llKruMcWqXMZyJeHX-VZLq8BBG', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1Nq2P4psHo_ZUy3tzF2xxppOuSqZzer0a', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1LYMwUWDclz6H_bwlcOPjxG1-v6UIP1Lr', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1EwG1aOflt7friyPOMe25COnoflAc8NCM', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1mO-SgLXd_y_AouFdq3MuywXfTkRindse', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1K20aRm_g65ly6Feo7VBeT9LlORFWJGE_', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['17f7Vewipl3NuCMfSzA66qCEE6Q4xQx0i', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1xSSLz9QIV78GmnrJQAqtK2pL2vdvYYXT', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1c9uui2OhVNF_J2iYvlqrLmqOXnjQd1lH', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['14Rjrzh4uT9RraqY-afSSfiCrjrzj04V6', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1DVUkM8_odEo21ecHkSNuQtReyQXXSbVI', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1gsFDpwbdaZvr9KIYYdTtZclycvB0DlJ8', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['163rJYnymSkYTGT4mQbSTXVSHJJAFVWpz', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1tsplOU9ho4R-xxPnYu3THBuAiQAhCZai', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1J-zgaGc5D-OaY8SwWa_Wsmnf5djRhhn5', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1GwBoHJUKsixPrNP7vif8DV7qJJKzH5FA', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1Pe1znTs4FI-AoVEBKPV4FRzTapNybpdr', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['103wMss9sjzgoQob_3-sB66TjmrBq0rsW', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1Li4MT28Z7rSm1oyeWaIR-f84HmYccqfB', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1JTZDxTliouUMfJSi4HbC8NMnCBT24MUa', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1ZF4T5XuXj3_YHp124O2HBXYC50cNbGyL', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1tyIkQbBg0Ix2Wy47da7D8kYSPqU0LsD2', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1naUSHdv3iDpXqLPnxR3GTW0D8si-h5Eo', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1F2d9IbgBpDWFtI5pMtFl0xJcg8zI-Qkg', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1wW2BJu1M-j1tkDqrIGRtKpj02_-I1641', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1Xgt8bKsxGJ7Za5cv7Rjt_NczjI3fhxs9', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1gG3wWAIZsdDRTIN70HSweikLp4lUJ7RR', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1aEuf7Q9FILBSRuDgkSK5QQ7EffvTI9z8', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1M8L-n3P7mYoPSE1YsQR2HfvDtx3efnD4', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1dM3k3m6prSDGUaUgu2GiTbKiW8J1tWfA', '1bRFOwuRvftDmNxk9nLwkggCo0XXDSroN'],
  ['1llyfMIQQDBsaEhrVHmN0RiCeUJwAokZM', '1aU-7mwSaDNVpGQyjy8-rbV608evLfpln'],
  ['1SsXVQI8iMgbIqxJuyZSMj47S2qr2khvX', '1hK7XUSexcYWyCTFXYUp1do84UtQmUyIX'],
  ['1C3p9fl9VCJO5c624ovJrXW2sXfSsYZDI', '1hK7XUSexcYWyCTFXYUp1do84UtQmUyIX'],
  ['1KLrg4eX-hafU8oBDQE_2tWdvbIkk58G5', '1O6cHvsqq-3HcOtwNfQ1OeMV0XPwqf6AB'],
  ['1jvqj63D7G8DF7feRZ5zS9XCEJWRDmcdS', '1G9F8xzLdXeG_Bigyw9VRnhErBkrM10x9'],
  ['1gUbP_Rb-SgkCMBa79sk79IqdAoJmit1B', '1Nv42J5Ksy4fbQsvkYJUATaBYy7VOMQ5p'],
  ['1GcXblKpaLcpi8Pevq6W6qISgdYu4OdSP', '1Rd6OBs92TavmZUkfU5VmoGDU55wq8q8V']
];

function _getOrCreatePasta_(mae, nome) {
  var it = mae.getFoldersByName(nome);
  return it.hasNext() ? it.next() : mae.createFolder(nome);
}

function quarentenarCrossTreeDefinitivo() {
  var mae = DriveApp.getFolderById(PROJETO_RAIZ_ID);
  var legado = _getOrCreatePasta_(mae, QUARENTENA_RAIZ_NOME);
  var quarent = _getOrCreatePasta_(legado, QUARENTENA_NOME);
  var qid = quarent.getId();
  var movidos = 0, jaLa = 0, multiPai = 0, sumidos = 0, falhas = 0;
  for (var i = 0; i < DUPS.length; i++) {
    var did = DUPS[i][0];
    var f;
    try { f = DriveApp.getFileById(did); f.getName(); }
    catch (e) { sumidos++; continue; }                       // já excluído, movido ou inacessível: nada a fazer
    // idempotência: já está na quarentena (esta ou de rodada anterior)?
    var pais = f.getParents(), nPais = 0, dentro = false;
    while (pais.hasNext()) {
      var p = pais.next(); nPais++;
      if (p.getId() === qid || p.getName().indexOf('_quarentena-cross') === 0) dentro = true;
    }
    if (dentro) { jaLa++; continue; }
    if (nPais > 1) { Logger.log('MULTI-PAI (resolver à mão): %s (%s)', f.getName(), did); multiPai++; continue; }
    try { f.moveTo(quarent); movidos++; }
    catch (e) { Logger.log('FALHA %s: %s', did, e); falhas++; }
  }
  Logger.log('=== DEFINITIVO CONCLUÍDO ===');
  Logger.log('Movidos agora: %s | Já na quarentena: %s | Multi-pai (manual): %s | Inexistentes: %s | Falhas: %s',
             movidos, jaLa, multiPai, sumidos, falhas);
  Logger.log('Pasta de quarentena: %s', quarent.getUrl());
}
