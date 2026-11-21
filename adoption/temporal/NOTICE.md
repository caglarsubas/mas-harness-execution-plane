# EXEC-TEMPORAL-PINS-001: licence and notice review

Pinned 2026-11-20T16:01:51Z for Linux AMD64: Temporal server 1.32.2 (upstream release binary) and the Python SDK temporalio 1.36.0 with
its closure. Each licence is read from the artifact's own metadata and licence files (verify_fetch.py inside the fetch
job, offline), not from an adoption view. Nothing is installed or selectable by this record.

| Artifact | Licence | Basis | Licence files |
|---|---|---|---|
| temporal_1.32.2_linux_amd64.tar.gz | MIT | derived: the LICENSE text at tag v1.32.2 (text from R10 mck7c object_6aab9afd99ceb1dc.txt, sha256 equal to the pin; object verified by R10 mck7b mirror_check.json 08f68243, manifest 44df609f, object record e8da948e) equals the MIT licence body exactly after SPDX-style normalisation (copyright lines removed, case, quotes and whitespace folded; match_licence.py ade8f97d, its reference MIT body typed, not fetched; checked by reviewer against the SPDX MIT text); copyright holders Temporal Technologies Inc. (2025) and Uber Technologies, Inc. (2020) | LICENSE at tag v1.32.2 (one named read) (sha256 6aab9afd99ceb1dcaf6a0d91386b46baef9bce17ae4006044e0f231e31430b69, 1152 B) |
| checksums.txt | MIT | release asset of the same server release; derived: the LICENSE text at tag v1.32.2 (text from R10 mck7c object_6aab9afd99ceb1dc.txt, sha256 equal to the pin; object verified by R10 mck7b mirror_check.json 08f68243, manifest 44df609f, object record e8da948e) equals the MIT licence body exactly after SPDX-style normalisation (copyright lines removed, case, quotes and whitespace folded; match_licence.py ade8f97d, its reference MIT body typed, not fetched; checked by reviewer against the SPDX MIT text); copyright holders Temporal Technologies Inc. (2025) and Uber Technologies, Inc. (2020) | LICENSE at tag v1.32.2 (one named read) (sha256 6aab9afd99ceb1dcaf6a0d91386b46baef9bce17ae4006044e0f231e31430b69, 1152 B) |
| temporalio-1.36.0-cp311-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl | MIT | wheel METADATA License-Expression | LICENSE (sha256 d7706f28d144dabf07e4946553a4d117d1dab5cda6bf34a602959b4a2fa86b38, 1108 B); temporalio/bridge/sdk-core/LICENSE.txt (sha256 cf8fe04521deeb6f99f644570bc8bee71c11dc410dbb72bccfb3a51829860c7b, 1108 B); temporalio/bridge/sdk-core/crates/protos/protos/api_cloud_upstream/LICENSE (sha256 aa36e2ca5072852dcd13c9d7c126fde1ceca44e0695df8b6438641a60e12e132, 1109 B); temporalio/bridge/sdk-core/crates/protos/protos/api_upstream/LICENSE (sha256 dfab09792f0b0df7b589581f87654f7da8f6c191145c4d3e994f35027a85e193, 1108 B); temporalio-1.36.0.dist-info/licenses/LICENSE (sha256 d7706f28d144dabf07e4946553a4d117d1dab5cda6bf34a602959b4a2fa86b38, 1108 B) |
| nexus_rpc-1.5.0-py3-none-any.whl | MIT | wheel METADATA License-Expression | nexus_rpc-1.5.0.dist-info/licenses/LICENSE (sha256 7903f782a1ff13735788ba9476b3d3976c37a8921c5dd144b6894eb45f2ebf5f, 1102 B) |
| protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl | BSD-3-Clause | derived from wheel METADATA License '3-Clause BSD License' and the hashed licence file | protobuf-7.36.2.dist-info/LICENSE (sha256 6e5e117324afd944dcf67f36cf329843bc1a92229a8cd9bb573d7a83130fea7d, 1732 B) |
| types_protobuf-7.35.1.20260906-py3-none-any.whl | Apache-2.0 | wheel METADATA License-Expression | types_protobuf-7.35.1.20260906.dist-info/licenses/LICENSE (sha256 295f8538c94ae5c3043301cf7cff1c852dab6a786a8ddee471e061b40d5ecabe, 12657 B) |
| typing_extensions-4.16.0-py3-none-any.whl | PSF-2.0 | wheel METADATA License-Expression | typing_extensions-4.16.0.dist-info/licenses/LICENSE (sha256 3b2f81fe21d181c499c59a256c8e1968455d6689d269aa85373bfb6af41da3bf, 13936 B) |

## Notes

- Server: the release archive holds no licence-named member ("not in the archive"). The licence is read from the
  LICENSE file of temporalio/temporal at tag v1.32.2, fetched once by owner approval into the mirror
  (sha256 6aab9afd99ceb1dcaf6a0d91386b46baef9bce17ae4006044e0f231e31430b69, 1152 B) and read back by R10's mirror-read job: mck7b mirror_check.json 08f68243 (manifest 44df609f,
  ok 1/1) and object record e8da948e; the text itself came from mck7c object_6aab9afd99ceb1dc.txt, whose sha256 equals
  the pin above.
- The MIT identifier is derived by match_licence.py: the reference MIT body in it was typed, not fetched, and is checked
  by the reviewer against the SPDX MIT text.
- checksums.txt is a release asset of the same server release and carries no licensed code of its own.
- temporalio bundles the Rust sdk-core and its protocol definitions; their licence files are listed with the wheel's,
  each by its own digest.
- Compatibility of temporalio 1.36.0 with server 1.32.2 is not stated by the artifacts; it is proven by
  EXEC-TEMPORAL-001's integration test before the provider can become selectable.
