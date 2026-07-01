# Group Chat Status Message

成员 A 的数据工作已经完成，所有数据、EDA、schema、split policy 和论文 Data
材料都在 `member_A_deliverables/`。Sankeerth Adisha 负责生成管线，请直接让 LLM
读取并执行
`member_A_deliverables/handoffs/member_B_prompting_pipeline.md`；他会独立完成
zero-shot、three-shot 和 self-refinement，并使用自己本地的 CEFR critic，不需要等待
David。David Kim 负责最终评估，请直接让 LLM 读取并执行
`member_A_deliverables/handoffs/member_C_evaluation_pipeline.md`；他可以立即用
identity/synthetic 数据完成评估代码，也不需要等待 Sankeerth。两人的唯一依赖是：
Sankeerth 完成后把冻结的 prediction、manifest 和 SHA-256 hash 交给 David，David
验证 hash 后独立重新计算最终 CEFR 和 semantic metrics，不能直接复用 Sankeerth
critic 的分数。等 B/C 结果完成后，Shaohua Liu 让 LLM 读取
`member_A_deliverables/handoffs/member_D_paper_integration.md`，整合 A/B/C
材料并完成四页 preliminary paper。
