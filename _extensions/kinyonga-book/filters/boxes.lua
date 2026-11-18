-- Boxes of a book written as `::: remarkbox`, `::: pitfall` or the `ark-concept`, `ark-activity`, `ark-tip`, `ark-mistake`
-- and `ark-example` set, each with a leading `[Title]{.remark-title}` (or `.pitfall-title`, `.ark-*-title`) span. The web edition styles them with CSS; for the print editions this filter turns them
-- into Quarto callouts (a note, a tip and an important box, made with quarto.Callout), so the LaTeX and Typst writers draw them in the brand colours. Without it
-- Pandoc gives the Div no environment and the box reaches the PDF as loose text.

-- Colours of the LaTeX box, as names from tokens/colors.tex: accent edge, fill and title colour.
local LATEX = {
  note = { "knBlue", "knTintBlue", "knBlue" },
  tip = { "knSuccess", "knTintGreen", "knGreenInk" },
  important = { "knDanger", "knTintRed", "knRedDeep" },
}

local KINDS = {
  remarkbox = { callout = "note", fallback = "Remark", title = "remark-title" },
  pitfall = { callout = "important", fallback = "Pitfall", title = "pitfall-title" },
  ["ark-concept"] = { callout = "note", fallback = "Key Concept", title = "ark-concept-title" },
  ["ark-activity"] = { callout = "tip", fallback = "Activity", title = "ark-activity-title" },
  ["ark-tip"] = { callout = "tip", fallback = "Pro Tip", title = "ark-tip-title" },
  ["ark-mistake"] = { callout = "important", fallback = "Common Mistake", title = "ark-mistake-title" },
  ["ark-example"] = { callout = "note", fallback = "Example", title = "ark-example-title" },
}

local function take_title(blocks, class)
  local first = blocks[1]
  if first and (first.t == "Para" or first.t == "Plain") then
    for _, inline in ipairs(first.content) do
      if inline.t == "Span" and inline.classes:includes(class) then
        table.remove(blocks, 1)
        return pandoc.utils.stringify(first)
      end
    end
  end
  return nil
end

function Div(el)
  if FORMAT:match("html") then
    return nil
  end
  for _, class in ipairs(el.classes) do
    local kind = KINDS[class]
    if kind then
      local title = take_title(el.content, kind.title) or kind.fallback
      if FORMAT:match("latex") then
        local c = LATEX[kind.callout]
        local open = string.format("\\begin{knbox}{%s}{%s}{%s}{%s}", c[1], c[2], c[3], (title:gsub("([&%%%$#_{}])", "\\%1")))
        table.insert(el.content, 1, pandoc.RawBlock("latex", open))
        table.insert(el.content, pandoc.RawBlock("latex", "\\end{knbox}"))
        return el
      end
      return quarto.Callout({ type = kind.callout, title = title, content = el.content, appearance = "default", icon = false })
    end
  end
  return nil
end
