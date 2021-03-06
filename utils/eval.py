import torch

from .helper import subsequent_mask


def evaluate(config, input_seq, tokenizer, model, device, verbose=True):
    model.eval()
    ids = tokenizer.encode(input_seq)
    src = torch.tensor(ids, dtype=torch.long, device=device).view(1, -1)
    src_mask = torch.ones(src.size(), dtype=torch.long, device=device)
    mem = model.encode(src, src_mask)
    ys = torch.ones(1, 1).fill_(tokenizer.cls_token_id).long().to(device)
    with torch.no_grad():
        for i in range(config.max_len - 1):
            out = model.decode(mem, src_mask,
                               ys, subsequent_mask(ys.size(1)).type_as(ys))
            prob = model.generate(out[:, -1])
            _, next_word = torch.max(prob, dim=1)
            next_word = next_word[0]
            if next_word == tokenizer.sep_token_id:
                break
            ys = torch.cat([ys, torch.ones(1, 1).type_as(ys).fill_(next_word).long()], dim=1)
    ys = ys.view(-1).detach().cpu().numpy().tolist()[1:]
    text = tokenizer.decode(ys)
    if verbose:
        print(tokenizer.decode(ys))
    return text
