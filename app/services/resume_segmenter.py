"""
Resume Segmentation Service.
Splits resume text into semantic sections (Skills, Experience, Projects)
to enable weighted skill extraction.
"""
import re
from typing import Dict, List, Tuple
from enum import Enum

class SectionType(Enum):
    PRIMARY = "PRIMARY"       # Skills, Technologies, Technical Skills
    SECONDARY = "SECONDARY"   # Experience, Projects, Work History
    TERTIARY = "TERTIARY"     # Summary, Education, Achievements, Certifications
    UNKNOWN = "UNKNOWN"

class ResumeSegmenter:
    """
    Segments resume text into semantic sections.
    Identify "Primary" sections (high trust) vs "Secondary" (needs verification).
    """
    
    # Headers that indicate a Primary section (High Trust)
    PRIMARY_HEADERS = {
        r"skills?", r"technical skills?", r"technologies", r"tech stack", 
        r"core competencies", r"expertise", r"programming languages",
        r"tools & technologies", r"technology stack"
    }
    
    # Headers that indicate Secondary section (Medium Trust - needs confirmation)
    SECONDARY_HEADERS = {
        r"experience", r"work experience", r"employment", r"professional experience",
        r"work history", r"projects?", r"personal projects?", r"key projects"
    }
    
    # Headers that indicate Tertiary section (Low Trust - likely noise)
    TERTIARY_HEADERS = {
        r"summary", r"profile", r"about me", r"education", r"achievements?", 
        r"certifications?", r"awards?", r"interests?", r"languages?", # Spoken languages
        r"references?", r"volunteer", r"publications?"
    }
    
    # Line-level patterns that promote content to PRIMARY trust (even inside Secondary sections)
    # e.g., "Technologies: Python, React" line inside a Project description
    PRIMARY_LINE_PATTERNS = [
        r"^(?:technologies|tech stack|built with|tools|stack)\s*[:\-]", 
        r"environment\s*[:\-]"
    ]
    
    def segment(self, text: str) -> Dict[SectionType, List[str]]:
        """
        Segment text into classified content blocks.
        
        Returns:
            Dict mapping SectionType to list of text content strings.
        """
        if not text:
            return {t: [] for t in SectionType}
        
        lines = text.split('\n')
        segments = {t: [] for t in SectionType}
        
        current_type = SectionType.UNKNOWN
        current_buffer = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Check if this line is a header
            new_type = self._detect_header(stripped)
            
            if new_type:
                # Flush previous buffer to previous section
                if current_buffer:
                    segments[current_type].append('\n'.join(current_buffer))
                    current_buffer = []
                
                current_type = new_type
                # header line itself usually doesn't contain skills, but add it just in case
                # or skip it to avoid matching header words? 
                # Better to skip common headers, but "Technical Skills: Python" is possible
                if ':' in stripped:
                    current_buffer.append(stripped)
            else:
                # Check for line-level promotion (e.g., "Tech Stack: ...")
                if self._is_primary_line(stripped):
                    # Add this specific line as PRIMARY content
                    segments[SectionType.PRIMARY].append(stripped)
                else:
                    current_buffer.append(stripped)
        
        # Flush final buffer
        if current_buffer:
            segments[current_type].append('\n'.join(current_buffer))
            
        return segments
    
    def _detect_header(self, line: str) -> SectionType | None:
        """Detect if a line looks like a section header."""
        # Heuristics: Short line, few words, maybe all caps or title case
        if len(line.split()) > 5:
            return None
            
        line_lower = line.lower().strip(':').strip()
        
        for pattern in self.PRIMARY_HEADERS:
            if re.fullmatch(pattern, line_lower):
                return SectionType.PRIMARY
                
        for pattern in self.SECONDARY_HEADERS:
            if re.fullmatch(pattern, line_lower):
                return SectionType.SECONDARY
                
        for pattern in self.TERTIARY_HEADERS:
            if re.fullmatch(pattern, line_lower):
                return SectionType.TERTIARY
                
        return None

    def _is_primary_line(self, line: str) -> bool:
        """Check if a single line should be treated as Primary trust source."""
        line_lower = line.lower()
        for pattern in self.PRIMARY_LINE_PATTERNS:
            if re.search(pattern, line_lower):
                return True
        return False
