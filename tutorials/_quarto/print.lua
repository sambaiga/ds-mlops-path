-- Web-only material has no place on paper: the badges of a chapter (Open in Colab, Download Notebook, Source on GitHub)
-- are images fetched from the web, and a link that holds only such an image is an empty link once the image is gone.
-- Run on the print formats only, before Quarto's own filters.

local function remote(src)
  return src:match("^https?://") ~= nil
end

function Image(el)
  if remote(el.src) then
    return {}
  end
end

function Link(el)
  if #el.content == 0 then
    return {}
  end
end

function Para(el)
  local blank = true
  for _, inline in ipairs(el.content) do
    if inline.t ~= "Space" and inline.t ~= "SoftBreak" and inline.t ~= "LineBreak" then
      blank = false
    end
  end
  if blank then
    return {}
  end
end

-- Terminal output carries escape sequences: colour codes (ESC [ 31 m), and the links that the rich logger writes
-- (ESC ] 8 ; id ; address ESC \). LaTeX cannot read any of them, so they are removed from every code block.
local function plain(text)
  text = text:gsub("\27%][^\27\7]*\27\\", "")
  text = text:gsub("\27%][^\27\7]*\7", "")
  text = text:gsub("\27%[[%d;?]*[A-Za-z]", "")
  return (text:gsub("\27", ""))
end

function CodeBlock(el)
  el.text = plain(el.text)
  return el
end

function RawBlock(el)
  if el.format == "html" then
    return {}
  end
end
